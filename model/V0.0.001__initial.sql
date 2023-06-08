alter table tinder.image 
   drop foreign key fk_image_reference_user;

alter table tinder.message 
   drop foreign key fk_message_reference_user_from;

alter table tinder.message 
   drop foreign key fk_message_reference_user_to;

alter table tinder.message 
   drop foreign key fk_message_reference_message_;

alter table tinder.message 
   drop foreign key fk_message_reference_pair;

alter table tinder.pair 
   drop foreign key fk_pair_reference_image;

alter table tinder.pair 
   drop foreign key fk_pair_reference_user;

alter table tinder.user 
   drop foreign key fk_user_reference_gender;

alter table tinder.user 
   drop foreign key fk_user_reference_zod_c;

alter table tinder.user 
   drop foreign key fk_user_reference_zod_s;

alter table tinder.user 
   drop foreign key fk_user_reference_choice;

drop table if exists tinder.choice;

drop table if exists tinder.gender;


alter table tinder.image 
   drop foreign key fk_image_reference_user;

drop table if exists tinder.image;


alter table tinder.message 
   drop foreign key fk_message_reference_pair;

alter table tinder.message 
   drop foreign key fk_message_reference_user_from;

alter table tinder.message 
   drop foreign key fk_message_reference_user_to;

alter table tinder.message 
   drop foreign key fk_message_reference_message_;

drop table if exists tinder.message;

drop table if exists tinder.message_plan;


alter table tinder.pair 
   drop foreign key fk_pair_reference_user;

alter table tinder.pair 
   drop foreign key fk_pair_reference_image;

drop table if exists tinder.pair;


alter table tinder.user 
   drop foreign key fk_user_reference_gender;

alter table tinder.user 
   drop foreign key fk_user_reference_zod_c;

alter table tinder.user 
   drop foreign key fk_user_reference_zod_s;

alter table tinder.user 
   drop foreign key fk_user_reference_choice;

drop table if exists tinder.user;

drop table if exists tinder.zodiac;

create table tinder.choice
(
   id                   tinyint not null  comment '',
   name                 varchar(20) not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

insert into tinder.choice values (1, 'dislike');
insert into tinder.choice values (2, 'like');
insert into tinder.choice values (3, 'superlike');

create table tinder.gender
(
   id                   tinyint not null  comment '',
   name                 varchar(10) not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

insert into tinder.gender values (0, 'male');
insert into tinder.gender values (1, 'female');
insert into tinder.gender values (-1, 'unknown');

create table tinder.image
(
   id                   integer not null auto_increment  comment '',
   user_id              char(24) not null  comment '',
   url                  varbinary(3072) not null  comment '',
   female_probability   decimal(21,20) not null  comment '',
   meta_timestamp       timestamp not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

alter table tinder.image
   add unique ak_key_2 (url);

create table tinder.message
(
   id                   varchar(255) not null  comment '',
   pair_id              char(48) not null  comment '',
   create_datetime      datetime not null  comment '',
   sent_from            char(24) not null  comment '',
   sent_to              char(24) not null  comment '',
   message              varchar(10000) not null  comment '',
   message_plan_id      integer not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

create table tinder.message_plan
(
   message_plan_id      integer not null auto_increment  comment '',
   plan_id              integer not null  comment '',
   message_num          integer(255) not null  comment '',
   message_template     varchar(255)  comment '',
   primary key (message_plan_id)
);

create table tinder.pair
(
   id                   char(48) not null  comment '',
   user_id              char(24) not null  comment '',
   create_datetime      datetime not null  comment '',
   image_id             integer  comment '',
   is_super_like        boolean not null  comment '',
   is_super_boost_match boolean not null  comment '',
   is_experiences_match boolean not null  comment '',
   is_fast_match        boolean not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

create table tinder.user
(
   id                   char(24) not null  comment '',
   name                 varchar(50) not null  comment '',
   gender_id            tinyint not null  comment '',
   birth_date           date  comment '',
   city                 varchar(100)  comment '',
   job                  varchar(100)  comment '',
   school               varchar(255)  comment '',
   biography            text  comment '',
   zodiac_id_specified  tinyint  comment '',
   zodiac_id_calculated tinyint  comment '',
   is_verified          boolean not null  comment '',
   is_online            boolean  comment '',
   choice_id            tinyint  comment '',
   meta_datetime_create datetime not null default current_timestamp  comment '',
   meta_datetime_updae  datetime default current_timestamp on update current_timestamp  comment '',
   primary key (id)
)
default character set = utf8mb4;

create table tinder.zodiac
(
   id                   tinyint not null  comment '',
   name_eng             varchar(20) not null  comment '',
   name_rus             varchar(20) not null  comment '',
   primary key (id)
)
default character set = utf8mb4;

insert into tinder.zodiac values (1, 'sagittarius', 'стрелец');
insert into tinder.zodiac values (2, 'capricorn', 'козерог');
insert into tinder.zodiac values (3, 'aquarius', 'водолей');
insert into tinder.zodiac values (4, 'pisces', 'рыбы');
insert into tinder.zodiac values (5, 'aries', 'овен');
insert into tinder.zodiac values (6, 'taurus', 'телец');
insert into tinder.zodiac values (7, 'gemini', 'близнецы');
insert into tinder.zodiac values (8, 'cancer', 'рак');
insert into tinder.zodiac values (9, 'leo', 'лев');
insert into tinder.zodiac values (10, 'virgo', 'дева');
insert into tinder.zodiac values (11, 'libra', 'весы');
insert into tinder.zodiac values (12, 'scorpio', 'скорпион');

alter table tinder.image add constraint fk_image_reference_user foreign key (user_id)
      references tinder.user (id) on delete restrict on update restrict;

alter table tinder.message add constraint fk_message_reference_user_from foreign key (sent_from)
      references tinder.user (id) on delete restrict on update restrict;

alter table tinder.message add constraint fk_message_reference_user_to foreign key (sent_to)
      references tinder.user (id) on delete restrict on update restrict;

alter table tinder.message add constraint fk_message_reference_message_ foreign key (message_plan_id)
      references tinder.message_plan (message_plan_id) on delete restrict on update restrict;

alter table tinder.message add constraint fk_message_reference_pair foreign key (pair_id)
      references tinder.pair (id) on delete restrict on update restrict;

alter table tinder.pair add constraint fk_pair_reference_image foreign key (image_id)
      references tinder.image (id) on delete restrict on update restrict;

alter table tinder.pair add constraint fk_pair_reference_user foreign key (user_id)
      references tinder.user (id) on delete restrict on update restrict;

alter table tinder.user add constraint fk_user_reference_gender foreign key (gender_id)
      references tinder.gender (id) on delete restrict on update restrict;

alter table tinder.user add constraint fk_user_reference_zod_c foreign key (zodiac_id_calculated)
      references tinder.zodiac (id) on delete restrict on update restrict;

alter table tinder.user add constraint fk_user_reference_zod_s foreign key (zodiac_id_specified)
      references tinder.zodiac (id) on delete restrict on update restrict;

alter table tinder.user add constraint fk_user_reference_choice foreign key (choice_id)
      references tinder.choice (id) on delete restrict on update restrict;

