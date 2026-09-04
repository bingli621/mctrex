import mcstasscript as ms

trex = ms.McStas_instr(
    "TRex",
    author="Bing Li",
    origin="DMSC",
    input_path="./src/test_files/mcstas",
    output_path="./src/test_files/mcstas/out",
)

off_1 = trex.add_component("off_1", "File")
off_1.set_parameters(filename=' "off_1.off"', metadatakey='"geometry"', keep=0)

off_1.set_c_code_after(
    """METADATA off geometry %{
OFF
# guide 1
8 4 0
0.04294097009390828 -0.014978283933760675 1.895927
-0.047 -0.014978283933760675 1.895927
-0.047 0.014978283933760675 1.895927
0.04294097009390828 0.014978283933760675 1.895927
0.038777153448715 -0.016416851555439725 2.4550259113311768
-0.047 -0.016416851555439725 2.4550259113311768
-0.047 0.016416851555439725 2.4550259113311768
0.038777153448715 0.016416851555439725 2.4550259113311768
4 0 4 7 3 1.5 3.0 0.001 # left
4 1 5 6 2 1.5 3.0 0.001 # right
4 3 7 6 2 4.0 3.0 0.001 # top
4 0 4 5 1 4.0 3.0 0.001 # bottom
%}"""
)

guide = trex.add_component("guide_1", "Guide_anyshape_r")
guide.set_parameters(geometry='"{}"'.format("off_1.off"))

trex.settings(checks=True)
trex.backengine()
