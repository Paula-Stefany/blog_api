create database blog
default character set utf8mb4
default collate utf8mb4_general_ci;

create table if not exists autores (
id_autor int not null auto_increment,
nome varchar(60) not null,
email varchar(60) unique not null,
biografia text,
salt varchar(60),
senha_hash varchar(100) not null,
primary key(id_autor)
) engine = innodb;

create table if not exists postagens(
id_postagem int not null auto_increment,
id_autor int,
titulo varchar(60) not null,
assunto text,
primary key(id_postagem),
foreign key(id_autor) references autores(id_autor)
)engine = innodb;

create table if not exists administradores(
id_admin int not null auto_increment,
nome varchar(60) unique not null,
email varchar(60) unique not null,
salt varchar(60) not null,
senha_hash varchar(100) not null,
primary key(id_admin)
)engine = innodb;
