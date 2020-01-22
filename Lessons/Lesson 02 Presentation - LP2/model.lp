\* Source Pyomo model name=Wyndor *\

max 
profit:
+3 x(drs)
+5 x(wdw)

s.t.

c_u_Constraint3_:
+3 x(drs)
+2 x(wdw)
<= 18

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
   0 <= x(drs) <= 4
   0 <= x(wdw) <= 6
end
