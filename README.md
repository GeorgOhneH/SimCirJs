# "Von Neumann Maschines" simulations in SimCirJs
## Instructions Set
| # | Instructions | Command     | Note         |
|---|-------------|--------------|--------------|
| 0|  0000       | ADD Constant |  |
| 1| 0001        | ADD Register |  |
| 2| 0010        | SUB Constant |  |
| 3| 0011        | SUB Register |  |
| 4| 0100        | MUL Constant |  |
| 5| 0101        | MUL Register |  |
| 6| 0110        | DIV Constant |  |
| 7| 0111        | DIV Register |  |
| 8| 1000        | LOD Constant |  |
| 9| 1001        | LOD Register |  |
|10| 1010        | STO Register | Be careful not to overwrite something important |
|11| 1011        | JMP Constant |  |
|12| 1100        | JMZ Constant |   |
|13| 1101        |  NOP         | Be awary that every command uses 2 Bytes |
|14| 1110        |  HLT         | Be awary that every command uses 2 Bytes |