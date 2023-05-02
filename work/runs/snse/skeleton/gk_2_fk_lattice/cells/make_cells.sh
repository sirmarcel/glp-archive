vibes utils make-supercell -dd 2 4 4 geometry.in.primitive
vibes utils make-supercell -dd 3 6 6 geometry.in.primitive
vibes utils make-supercell -dd 4 8 8 geometry.in.primitive
vibes utils make-supercell -dd 5 10 10 geometry.in.primitive
vibes utils make-supercell -dd 6 12 12 geometry.in.primitive

vibes utils create-samples geometry.in.primitive.supercell_256 -T 300
vibes utils create-samples geometry.in.primitive.supercell_864 -T 300
vibes utils create-samples geometry.in.primitive.supercell_2048 -T 300
vibes utils create-samples geometry.in.primitive.supercell_4000 -T 300
vibes utils create-samples geometry.in.primitive.supercell_6912 -T 300