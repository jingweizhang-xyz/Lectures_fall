/* Decision variables */
var x1;
var x2;
var x3;
var d12 = -3;
var d13 = -2;
var d23 = 1;
var ve12 >= 0;
var ve13 >= 0;
var ve23 >= 0;

/* Objective function */
minimize answer: ve12 + ve13 + ve23;

/* Constraints */
s.t. firstU	:	x1 - x2 - d12 <= ve12;
s.t. firstU	:	x1 - x2 - d12 >= -ve12;
s.t. secondU	:	x1 - x3 - d13 <= ve13;
s.t. secondL	:	x1 - x3 - d13 >= -ve13;
s.t. thirdU	:	x2 - x3 - d23 <= ve23;
s.t. thirdL	:	x2 - x3 - d23 >= -ve23;

end;