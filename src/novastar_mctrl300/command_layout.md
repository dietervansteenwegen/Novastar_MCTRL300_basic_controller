# Checksum:
* Sum of [byte 3]:[byte x -2] (all data except header)
* Add 0h5555

_Example:_
* Message = 55h AAh 00h 32h FEh 00 01 00 00 00 00 00 00 00 00 0Ah 00 01 91h 56h
* Calculation: 32h + FEh +1+Ah+1+5555h = 5691h

-> byte [x-1] = 91h, byte [x] = 56h

# Request/command:

| Byte | Meaning                                | Fixed                             |
| ---- | -------------------------------------- | --------------------------------- |
| 1    | Header (1)                             | 55h                               |
| 2    | Header (2)                             | AAh                               |
| 3    | ACK (Not used for req)                 | 00h                               |
| 4    | Serial number (=CMD number, see *)     | /                                 |
| 5    | Source address                         | FEh for computer                  |
| 6    | Dest address                           | /                                 |
| 7    | Card device type                       | 00h: send, 01h rx, 02h: function  |
| 8    | Port address (RJ45 output of sending?) | 00h for OUT1, 01h for OUT2        |
| 9    | Board address LSB (starts at 0)        | /                                 |
| 10   | Board address MSB                      | /                                 |
| 11   | Cmd type                               | 00h for read, 01h for write       |
| 12   | Reserved                               | 00h                               |
| 13   | Unit address [7:0]   (see **)          | /                                 |
| 14   | Unit address [15:8]                    | /                                 |
| 15   | Unit address [23:16]                   | /                                 |
| 16   | Unit address [31:24]                   | /                                 |
| 17   | Data length LSB                        | if CMD type = 01h: length of cmd  |
| 18   | Data length MSB                        | if CMD type ==00h: length of read |
| 19   | Data                                   | /                                 |
| xx   | Data                                   | /                                 |
| xx   | Data                                   | /                                 |
| xx   | Data                                   | /                                 |
| x-1  | Checksum LSB                           | /                                 |
| x    | Checksum MSB                           | /                                 |

(*): Any number to identify the command send and answer received. Can remain fixed if no new command is sent before an answer is received.

(**): referred as "offset(H)" in the control protocol documentation.


## Useful commands/registers/offset

| Address       | Length (bits) | Description        | Values                                                               |
| ------------- | ------------- | ------------------ | -------------------------------------------------------------------- |
| 0x02 00 01 01 | 8             | Test pattern       | 1: Off, 2:R, 3:G, 4:B, 5:Wh, 6:Hor, 7:Vertical, 8:Slash, 9:Grayscale |
| 0x02 00 00 01 | 8             | Overall brightness | 0-0xFF                                                               |


# Acknowledge or data Tx:

| Byte | Meaning                                | Fixed                                                                |
| ---- | -------------------------------------- | -------------------------------------------------------------------- |
| 1    | Header (1)                             | AAh                                                                  |
| 2    | Header (2)                             | 55h                                                                  |
| 3    | ACK (Not used for req)                 | 00 (succes), 01 (timeout), 02/03 (msg check error), 04 (invalid cmd) |
| 4    | Serial number (=CMD)                   | /                                                                    |
| 5    | Source address                         | FEh for computer                                                     |
| 6    | Dest address                           | FEh for computer                                                     |
| 7    | Card device type                       | 00: send, 01 rx, 02: function                                        |
| 8    | Port address (RJ45 output of sending?) | 00 (?)                                                               |
| 9    | Board address LSB (starts at 0)        | /                                                                    |
| 10   | Board address MSB                      | /                                                                    |
| 11   | 'code' or Cmd type                     | 00h for read (req data), 01h for write (send data)                   |
| 12   | Reserved                               | 00                                                                   |
| 13   | Unit address [7:0]                     | /                                                                    |
| 14   | Unit address [15:8]                    | /                                                                    |
| 15   | Unit address [23:16]                   | /                                                                    |
| 16   | Unit address [31:24]                   | /                                                                    |
| 17   | Data length LSB                        | if CMD type = 01h: length of cmd                                     |
| 18   | Data length MSB                        | if CMD type ==00h: length of read                                    |
| 19   | Data                                   | Does not exist if code ([ 11]) == 01                                 |
| xx   | Data                                   | /                                                                    |
| xx   | Data                                   | /                                                                    |
| xx   | Data                                   | /                                                                    |
| x-1  | Checksum LSB                           | /                                                                    |
| x    | Checksum MSB                           | /                                                                    |