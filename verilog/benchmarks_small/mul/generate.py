#!/usr/bin/env python3

ARange = ['16','16s','24','24s','32','32s','48','48s','64','64s','128','128s']
BRange = ['2','2s','4','4s','8','8s','16','16s','24','24s','32','32s','48','48s']
rtl = """(* top *)
module mul_{0}_{1}_{2}_{3} #(parameter AW={4}, BW={5}, AREG={6}, BREG={7}, PREG={8}) (input clk, CEA, CEB, CEP, input {9}[AW-1:0] A, input {10}[BW-1:0] B, output reg {11}[AW+BW-1:0] P);
reg {9}[AW-1:0] Ar;
reg {10}[BW-1:0] Br;
generate
    if (AREG) begin
        always @(posedge clk) if ({12}) Ar <= A;
    end
    else
        always @* Ar <= A;
    if (BREG) begin
        always @(posedge clk) if ({13}) Br <= B;
    end
    else
        always @* Br <= B;
    if (PREG) begin
        always @(posedge clk) if ({14}) P <= Ar * Br;
    end
    else
        always @* P <= Ar * Br;
endgenerate
endmodule"""

# https://stackoverflow.com/a/1482316
from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

for A in ARange:
    for B in BRange:
        for R in map(lambda i:''.join(i), powerset("ABP")): # Register existence
            for E in map(lambda i:''.join(i), powerset(R)): # Enable
                with open("mul_%s_%s_%s_%s.v" % (A,B,R,E), "w") as f:
                    print(rtl.format(A,B,R,E,A.rstrip('s'),B.rstrip('s'),
                        '1' if 'A' in R else '0', '1' if 'B' in R else '0', '1' if 'P' in R else '0',
                        'signed ' if 's' in A else '', 'signed ' if 's' in B else '', 'signed ' if 's' in A or 's' in B else '',
                        'CEA' if 'A' in E else '1', 'CEB' if 'B' in E else '1', 'CEP' if 'P' in E else '1'), file=f)
                if A != B:
                   with open("mul_%s_%s_%s_%s.v" % (B,A,R,E), "w") as f:
                        print(rtl.format(B,A,R,E,B.rstrip('s'),A.rstrip('s'),
                            '1' if 'B' in R else '0', '1' if 'A' in R else '0', '1' if 'P' in R else '0',
                            'signed ' if 's' in B else '', 'signed ' if 's' in A else '', 'signed ' if 's' in A or 's' in B else '',
                            'CEA' if 'B' in E else '1', 'CEB' if 'A' in E else '1', 'CEP' if 'P' in E else '1'), file=f)