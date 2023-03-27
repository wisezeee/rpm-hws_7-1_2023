create table population (
    id int generated always as identity primary key,
    population_ru text,
    population_en text,
    population_world text
);

insert into population (population_ru, population_en, population_world)
values ('143,4 million', '331,9 million', '7,888 milliard')