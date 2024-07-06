// Benchmark was created by MQT Bench on 2024-03-17
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 1.1.0
// Qiskit version: 1.0.2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
creg meas[8];
ry(-2.157666746655994) q[0];
ry(-4.211782825246222) q[1];
cz q[0],q[1];
ry(-1.2370557945339522) q[2];
cz q[0],q[2];
cz q[1],q[2];
ry(-1.835420271130908) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
ry(5.675448631303404) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
ry(1.992543527349273) q[5];
cz q[0],q[5];
cz q[1],q[5];
cz q[2],q[5];
cz q[3],q[5];
cz q[4],q[5];
ry(-3.9614120325075177) q[6];
cz q[0],q[6];
cz q[1],q[6];
cz q[2],q[6];
cz q[3],q[6];
cz q[4],q[6];
cz q[5],q[6];
ry(6.256558825358066) q[7];
cz q[0],q[7];
ry(0.9575112433700799) q[0];
cz q[1],q[7];
ry(-3.4409694019204746) q[1];
cz q[0],q[1];
cz q[2],q[7];
ry(-1.2871079310885394) q[2];
cz q[0],q[2];
cz q[1],q[2];
cz q[3],q[7];
ry(-5.212797392877597) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
cz q[4],q[7];
ry(5.7081388959152655) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
cz q[5],q[7];
ry(-2.09694650524312) q[5];
cz q[0],q[5];
cz q[1],q[5];
cz q[2],q[5];
cz q[3],q[5];
cz q[4],q[5];
cz q[6],q[7];
ry(0.03936263710907628) q[6];
cz q[0],q[6];
cz q[1],q[6];
cz q[2],q[6];
cz q[3],q[6];
cz q[4],q[6];
cz q[5],q[6];
ry(-3.482288199599529) q[7];
cz q[0],q[7];
ry(-4.850449052708141) q[0];
cz q[1],q[7];
ry(-3.316873998074638) q[1];
cz q[0],q[1];
cz q[2],q[7];
ry(2.4540261169005912) q[2];
cz q[0],q[2];
cz q[1],q[2];
cz q[3],q[7];
ry(4.487109865845744) q[3];
cz q[0],q[3];
cz q[1],q[3];
cz q[2],q[3];
cz q[4],q[7];
ry(-0.09125920106774732) q[4];
cz q[0],q[4];
cz q[1],q[4];
cz q[2],q[4];
cz q[3],q[4];
cz q[5],q[7];
ry(2.9938871913504315) q[5];
cz q[0],q[5];
cz q[1],q[5];
cz q[2],q[5];
cz q[3],q[5];
cz q[4],q[5];
cz q[6],q[7];
ry(5.352335782084085) q[6];
cz q[0],q[6];
cz q[1],q[6];
cz q[2],q[6];
cz q[3],q[6];
cz q[4],q[6];
cz q[5],q[6];
ry(-0.13680357214375327) q[7];
cz q[0],q[7];
ry(-6.257210313741039) q[0];
cz q[1],q[7];
ry(-1.8233232323012647) q[1];
cz q[2],q[7];
ry(5.423030744165693) q[2];
cz q[3],q[7];
ry(-0.25402447767616554) q[3];
cz q[4],q[7];
ry(-5.876085943475712) q[4];
cz q[5],q[7];
ry(3.4349277376346485) q[5];
cz q[6],q[7];
ry(2.1993284888364375) q[6];
ry(-5.776610711294471) q[7];
barrier q[0],q[1],q[2],q[3],q[4],q[5],q[6],q[7];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
measure q[3] -> meas[3];
measure q[4] -> meas[4];
measure q[5] -> meas[5];
measure q[6] -> meas[6];
measure q[7] -> meas[7];