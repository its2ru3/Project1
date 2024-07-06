// Benchmark was created by MQT Bench on 2024-03-17
// For more information about MQT Bench, please visit https://www.cda.cit.tum.de/mqtbench/
// MQT Bench version: 1.1.0
// Qiskit version: 1.0.2

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg meas[3];
creg meas0[3];
u2(-0.0866959008988637,-pi) q[0];
u2(-0.08676910416958972,-pi) q[1];
rzz(0.08633715978690501) q[0],q[1];
u2(-0.08663477981548695,-pi) q[2];
rzz(0.08631585680193811) q[0],q[2];
u3(2.2724822690290254,-1.1733017345370045,-pi/2) q[0];
rzz(0.08632192329635771) q[1],q[2];
u3(2.2724822690290254,-1.1756187639605353,-pi/2) q[1];
rzz(2.732743190113777) q[0],q[1];
u3(2.2724822690290254,-1.1713671304246889,-pi/2) q[2];
rzz(2.732068908179542) q[0],q[2];
u3(1.613215108868912,1.5693099928708039,pi/2) q[0];
rzz(2.732260924819353) q[1],q[2];
u3(1.6132151088689122,1.5719613991154286,pi/2) q[1];
rzz(-3.1271127960837783) q[0],q[1];
u3(1.613215108868912,1.5670962007746914,pi/2) q[2];
rzz(-3.126341206688792) q[0],q[2];
rx(-10.081529597185977) q[0];
rzz(-3.1265609337723994) q[1],q[2];
rx(-10.081529597185977) q[1];
rx(-10.081529597185977) q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas0[0];
measure q[1] -> meas0[1];
measure q[2] -> meas0[2];