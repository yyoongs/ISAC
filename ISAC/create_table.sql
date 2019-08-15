-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ISAC
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ISAC
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ISAC` DEFAULT CHARACTER SET utf8 ;
USE `ISAC` ;

-- -----------------------------------------------------
-- Table `ISAC`.`counsel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`counsel` (
  `id` INT NOT NULL,
  `counsel_id` CHAR(13) NOT NULL,
  `big_cate` VARCHAR(15) NOT NULL,
  `mid_cate` VARCHAR(15) NOT NULL,
  `small_cate` VARCHAR(15) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `question_date` DATETIME NOT NULL,
  `question` TEXT NOT NULL,
  `answer_date` DATETIME NULL,
  `answer` TEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`law`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`law` (
  `id` INT NOT NULL,
  `law_name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`counsel/law_resolve`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`counsel/law_resolve` (
  `id` INT NOT NULL,
  `counsel_id` INT NOT NULL,
  `law_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_law of counsel_counsel_idx` (`counsel_id` ASC) VISIBLE,
  INDEX `fk_law of counsel_law1_idx` (`law_id` ASC) VISIBLE,
  CONSTRAINT `fk_law of counsel_counsel`
    FOREIGN KEY (`counsel_id`)
    REFERENCES `ISAC`.`counsel` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_law of counsel_law1`
    FOREIGN KEY (`law_id`)
    REFERENCES `ISAC`.`law` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`Jo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`Jo` (
  `jo_id` INT NOT NULL,
  `jo_name` VARCHAR(100) NOT NULL,
  `jo_content` TEXT NOT NULL,
  `law_id` INT NOT NULL,
  PRIMARY KEY (`jo_id`),
  INDEX `fk_Jo_law1_idx` (`law_id` ASC) VISIBLE,
  CONSTRAINT `fk_Jo_law1`
    FOREIGN KEY (`law_id`)
    REFERENCES `ISAC`.`law` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`category` (
  `id` INT NOT NULL,
  `name` VARCHAR(50) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`solution_gijun`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`solution_gijun` (
  `id` INT NOT NULL,
  `trouble_type` VARCHAR(255) NOT NULL,
  `standard` VARCHAR(255) NULL,
  `bigo` TEXT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_solution_gijun_category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_solution_gijun_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `ISAC`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`item` (
  `id` INT NOT NULL,
  `name` VARCHAR(50) NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_item_category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_item_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `ISAC`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`precedent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`precedent` (
  `id` INT NOT NULL,
  `big_cate` VARCHAR(15) NULL,
  `mid_cate` VARCHAR(15) NULL,
  `small_cate` VARCHAR(15) NULL,
  `title` VARCHAR(45) NULL,
  `question_date` DATETIME NULL,
  `question` TEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`mobum_counsel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`mobum_counsel` (
  `id` INT NOT NULL,
  `big_cate` VARCHAR(15) NOT NULL,
  `mid_cate` VARCHAR(15) NOT NULL,
  `small_cate` VARCHAR(15) NULL,
  `title` VARCHAR(45) NOT NULL,
  `regis_date` DATETIME NOT NULL,
  `question` TEXT NOT NULL,
  `answer` TEXT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`counsel_item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`counsel_item` (
  `id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `counsel_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_counsel_item_item1_idx` (`item_id` ASC) VISIBLE,
  INDEX `fk_counsel_item_counsel1_idx` (`counsel_id` ASC) VISIBLE,
  CONSTRAINT `fk_counsel_item_item1`
    FOREIGN KEY (`item_id`)
    REFERENCES `ISAC`.`item` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_counsel_item_counsel1`
    FOREIGN KEY (`counsel_id`)
    REFERENCES `ISAC`.`counsel` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ISAC`.`counsel_precedent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`counsel_precedent` (
  `id` INT NOT NULL,
  `counsel_id` INT NOT NULL,
  `precendent_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_counsel_precedent_counsel1_idx` (`counsel_id` ASC) VISIBLE,
  INDEX `fk_counsel_precedent_precedent1_idx` (`precendent_id` ASC) VISIBLE,
  CONSTRAINT `fk_counsel_precedent_counsel1`
    FOREIGN KEY (`counsel_id`)
    REFERENCES `ISAC`.`counsel` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_counsel_precedent_precedent1`
    FOREIGN KEY (`precendent_id`)
    REFERENCES `ISAC`.`precedent` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `ISAC` ;

-- -----------------------------------------------------
-- Placeholder table for view `ISAC`.`view1`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ISAC`.`view1` (`id` INT);

-- -----------------------------------------------------
-- View `ISAC`.`view1`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ISAC`.`view1`;
USE `ISAC`;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
