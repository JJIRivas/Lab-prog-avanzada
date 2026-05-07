use std::time::Instant;
use std::cmp;
use rand::distr::Alphanumeric;
use rand::{self, RngExt};


const N_TABLA: usize = 211;

// Ocupamos enums para idenfiticar el tipo de hash con patter matching.
enum TiposHash{
    Bit,
    Base,
}
// Nota: structs y impl en rust son similar a una interfaz y la clase que implementa esta.
struct HashTable {
    cubetas: Vec<Vec<(String, usize)>>, //Es un Vector<Vector(...)> para hacer el "encadenamiento" si hay colisiones.
    colisiones: usize,
    elementos_total: usize,
    tipo_hash: TiposHash,
}

impl HashTable{
    fn create(tipos_hash: TiposHash) -> Self{
        let mut cubetas = Vec::new();

        for _ in 0..N_TABLA{
            cubetas.push(Vec::new());
        }

        HashTable {
            cubetas,
            colisiones: 0,
            elementos_total: 0,
            tipo_hash: tipos_hash
        }
    }

    /*  Funcion para sacar el hash segun los codigos numericos del str.
    .bytes() retorna un iterador en los bytes del str y wrapping_add es una manera
    de sumar los valores en la cual si el valor se pasa de 255 dara vuelta a 0 y seguira
    sumando desde ahi.
     */
    fn bit_hasher(&self, key: &str) -> usize{
        let mut suma: usize = 0;
        for byte in key.bytes(){
            suma = suma.wrapping_add(byte as usize);
        }
        suma % N_TABLA
    }

    /* Funcion para calcular el hash ocupando una base numerica de 31. Similar a la anterior
    en formato general.
     */
    fn base_hasher(&self, key: &str) -> usize{
        let mut suma: usize = 0;
        for byte in key.bytes(){
            suma = (suma * 31 + byte as usize) % N_TABLA;
        }
        suma
    }

    /* Funcion para insertar un valor en nuestra tabla.*/
    fn insertar(&mut self, key: String, value: usize) {
        /*Se define el tipo de hash que es y se llama a la funcion
        correspondiente. Esto es repetido harto asi que no se mencionara de nuevo.*/
        let llave = match self.tipo_hash {
            TiposHash::Bit => self.bit_hasher(&key),
            TiposHash::Base => self.base_hasher(&key),
        };

        /* Mediante un ciclo en el indice donde apunta la llave principal, se verifica
        si la llave principal y la "subllave" es igual, si es asi, se reemplaza el
        valor y termina. Iter_mut es para poder modificar el Vector como tal.
         */
        for par in self.cubetas[llave].iter_mut() {
            if par.0 == key {
                par.1 = value;
                return;
            }
        }

        /* Si llegamos aqui entonces no nos referimos a un valor que ya estaba, sino que
        ocurrio una colision. Se aumenta el contador de colisiones.
         */
        if !self.cubetas[llave].is_empty() {
            self.colisiones += 1;
        }

        /* Despues de aumentar el contador se empuja en la cola a la nueva dupla
        y se aumenta el contador de la cantidad de elementos totales.*/
        self.cubetas[llave].push((key, value));
        self.elementos_total += 1;
    }


    // Funcion que busca un valor y retorna este.
    fn buscar(&self, key: &str) -> Option<usize>{
        let llave: usize;
        match &self.tipo_hash {
            TiposHash::Bit => llave = self.bit_hasher(&key),
            TiposHash::Base => llave = self.base_hasher(&key),
        }

        /* En rust no se puede retornar "Null" o similar, sino que retornamos
        un enum que puede ser un valor (Some) o nada (None). De todas formas, si
        se encuentra en el lugar un valor y la llave es la misma, se retorna.*/
        for par in &self.cubetas[llave] {
            if par.0 == key {
                return Some(par.1);
            }
        }

        // Nuestro "Null".
        None
    }

    /* Funcion para borrar un valor segun la llave. */
    fn borrar(&mut self, key: String) -> bool{
        let llave: usize;
        match &self.tipo_hash {
            TiposHash::Bit => llave = self.bit_hasher(&key),
            TiposHash::Base => llave = self.base_hasher(&key),
        }

        /* Este es interesante. Ya que tenemos que modificar el array lo recorremos de
        una manera diferente con operaciones que permiten &mut. Primero tomamos la llave
        general y decimos que, si hay un valor cualquiera "pos" que cumpla el patron de buscar
        la cubeta como tal para coincidencias, entonces borramos ese elemento y quitamos uno del
        total. Aqui |par| funciona como un lambda, es decir, "para cada elemento par, revisa si par.0 == key".
        Entonces en general, la iteracion en la cubeta es igual a decir "recorre la cubeta y dame
        la posición del primer par cuya key sea igual a la key"*/

        let cubeta = &mut self.cubetas[llave];
        if let Some(pos) = cubeta.iter().position(|par| par.0 == key){
            cubeta.remove(pos);
            self.elementos_total -= 1;
            return true;
        }

        false
    }

    // Factor de carga. f64 para contar decimales.
    fn factor_carga(&self) -> f64 {
        return self.elementos_total as f64/N_TABLA as f64;
    }

    // Para todos los elementos, verifica si hay algo ahi y toma cuenta.
    fn cubetas_ocupadas(&self) -> usize {
        let mut ocupaciones: usize = 0;
        for cubeta in &self.cubetas{
            if !cubeta.is_empty() {ocupaciones += 1}
        }
        ocupaciones
    }

    /* Para todos los elementos, compara la cantidad de duplas que hay en cada uno
    y retorna el que tenga mas.
     */
    fn max_tam_cubetas(&self) -> usize{
        let mut maximo: usize = 0;
        for cubeta in &self.cubetas{ maximo = cmp::max(maximo, cubeta.len()); }
        maximo
    }

    // Retorna la informacion general.
    fn reporte(&self, tiempo: f64){
        let estrategia = match self.tipo_hash{
            TiposHash::Bit => "Bit",
            TiposHash::Base => "Base",
        };

        println!("
            Estrategia = {}
            Tamaño = {}
            Elementos = {}
            Factor de Carga = {}
            Colisiones = {}
            Cubetas Ocupadas = {}
            Tamaño maximo Cubetas = {}
            Tiempo de insercion = {}
            ",
            estrategia,
            N_TABLA,
            &self.elementos_total,
            &self.factor_carga(),
            &self.colisiones,
            &self.cubetas_ocupadas(),
            &self.max_tam_cubetas(),
            tiempo)
    }
}

/* Genera 1000 strings aleatorios de un tamaño maximo de 8 caracteres,
ocupa el crate de rand y un vector para tener los datos al final. */
fn strings_aleatorios () -> Vec<String> {
    let mut rng = rand::rng();
    let mut datos: Vec<String> = Vec::new();
    let mut palabra: String;

    /* El ciclo define que la palabra es el resultado de una iteracion random de
    caracteres alfanumericos, toma los 8 primeros valores random que devuelve y
    los transforma a string para luego "recollectar" todos los caracteres e insertar.
     */
    for pal in 0..1000{
        palabra = (&mut rng).sample_iter(Alphanumeric)
            .take(8)
            .map(char::from)
            .collect();
        datos.insert(pal, palabra);
    }
    datos
}

// Generacion de datos secuenciales.
fn datos_secuenciales() -> Vec<String>{
    let mut datos: Vec<String> = Vec::new();

    for i in 0..1000{
        datos.push(format!("user{}", i));
    }

    datos
}

// Generacion de datos agrupados.
fn datos_agrupados() -> Vec<String>{
    let mut datos: Vec<String> = Vec::new();

    for i in 0..1000{
        datos.push(format!("aaa{}",i));
    }

    datos
}

/* Funcion para empezar el experimento como tal.
Define dos tablas de tipo bit y base, luego ocupando el crate time toma el tiempo
de ejecucion de cada insercion. Es una iteracion con los datos para meter todos.
 */
fn empezar_experimento(nombre: &str, llaves: Vec<String>) {
    println!("\nDataset: {}", nombre);

    let mut tabla_bit = HashTable::create(TiposHash::Bit);
    let mut tabla_base = HashTable::create(TiposHash::Base);

    let inicio = Instant::now();
    for (i, llave) in llaves.iter().enumerate() {
        tabla_bit.insertar(llave.clone(), i);
    }
    tabla_bit.reporte(inicio.elapsed().as_secs_f64());

    let inicio = Instant::now();
    for (i, llave) in llaves.iter().enumerate() {
        tabla_base.insertar(llave.clone(), i);
    }
    tabla_base.reporte(inicio.elapsed().as_secs_f64());
}


fn main() {
    empezar_experimento("Aleatorio", strings_aleatorios());
    empezar_experimento("Secuencial", datos_secuenciales());
    empezar_experimento("Agrupado", datos_agrupados());
}
