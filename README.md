# von-neumann-maschine simulations in SimCirJs
## Instructions Set
| Instructions | Command     | Note         |
|-------------|--------------|--------------|
|  0000       | ADD Constant |  |
| 0001        | ADD Register |  |
| 0010        | SUB Constant |  |
| 0011        | SUB Register |  |
| 0100        | MUL Constant |  |
| 0101        | MUL Register |  |
| 0110        | DIV Constant |  |
| 0111        | DIV Register |  |
| 1000        | LOD Constant |  |
| 1001        | LOD Register |  |
| 1010        | STO Register | Be carful not to overwrite something important |
| 1011        | JMP Constant |  |
| 1100        | JMZ Constant |  |
| 1101        |  NOP         | Still uses 2 Bytes |
| 1110        |  HLT         |  |