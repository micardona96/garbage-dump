include "globals.mzn"; 
%%include "dat20_1.dzn";

%%Idea: distancias es un arreglo que va a contener las distancias entre cada una de las ciudades y la ubicación del 
%%relleno sanitario. De ese arreglo, se sacara el elemento más pequeño, puesto que es la distancia a la ciudad más 
%%cercana y ese valor es el que va a ser maximizado.

%%PARAMETROS
%%Parámetro que controla la precisión
int: precision = 10;
%%Longitud del cuadrado que representa la región EcoReg
int : n;
%%Cantidad de ciudades de la región
int : m;
%%Matriz con m filas y 2 columnas en cada una de ellas. En cada fila, la primera columa se trata de la
%%posición en el este (x) de la ciudad y la segunda de la posición en el norte (y)
array [1..m, 1..2] of 0..n : ciudades;


%%VARIABLES
%%Ubicación en el este del relleno sanitario
var 0..(n*precision) : pos_este ;
%%Ubicación en el norte del relleno sanitario
var 0..(n*precision) : pos_norte ;
%%Arreglo con las distancias entre cada ciudad y el relleno
array [1..m] of var 0.0..(2*n*precision) : distancias;

%%Restricciones
%%Rellenar distancias con la formula Manhattan
constraint forall([distancias[i] = (abs(ciudades[i,1] - (pos_este/precision)) + abs(ciudades[i,2] - (pos_norte/precision)))| i in 1..m]);


%%El valor mínimo en el arreglo de distancias como variable para maximizar
var 0.0..(2*n*precision): distancia = min(distancias);

%%Maximizar distancia a la ciudad más cercana
solve maximize distancia;

%%Salida
output ["{'n' :",show(n),",\n"];
output ["'m' :",show(m),",\n"];
output ["'ciudades' :",show(ciudades),",\n"];
output ["'distancias' :",show(distancias),",\n"];
output ["'pos_este' :",show(pos_este/precision),",\n"];
output ["'pos_norte' :",show(pos_norte/precision),"}"];
