from pxblat import fa_to_two_bit

fa_to_two_bit(
    ["test_ref.fa"],
    "test_ref.2bit",
    noMask=False,
    stripVersion=False,
    ignoreDups=False,
    useLong=False,
)
print("Done")
