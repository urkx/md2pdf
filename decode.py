from md2pdf.decode.deflate.block import Block, BlockHeader, BlockType

b = Block(BlockHeader(False, BlockType.DYN_COMPRESSION), "tres tristes tigres tragaban trigo en un trigal")
b.process()

