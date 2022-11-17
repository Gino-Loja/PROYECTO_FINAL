
CREATE DATABASE SISTEMA_RF;
CREATE TABLE IF NOT EXISTS estudiantes
(
    codigo varchar(15) NOT NULL,
    nombre varchar(120) NOT NULL,
    correo varchar(90)  NOT NULL,
    CONSTRAINT estudiantes_pkey PRIMARY KEY (codigo)
);



CREATE TABLE IF NOT EXISTS pao
(
    codigo_es varchar(15)  NOT NULL,
    pao_ varchar(2)  NOT NULL,
    CONSTRAINT pao_pkey PRIMARY KEY (codigo_es),
    CONSTRAINT pao_codigo_es_fkey FOREIGN KEY (codigo_es)
     REFERENCES estudiantes (codigo) 
        
);


CREATE TABLE IF NOT EXISTS carrera
(
    codigo_car varchar(15)  NOT NULL,
    carrera_ varchar(120)  NOT NULL,
    CONSTRAINT carrera_pkey PRIMARY KEY (codigo_car),
    CONSTRAINT carrera_codigo_car_fkey FOREIGN KEY (codigo_car)
        REFERENCES pao (codigo_es)
       
);




