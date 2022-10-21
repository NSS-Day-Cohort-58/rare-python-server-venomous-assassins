CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

ALTER TABLE "Posts" 
DROP COLUMN "approved"

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');


INSERT INTO `Users` VALUES (null, "Lorin", "Jones", "Lorin.Jones@gmail.com", "Hairbrained. Nuts. Hysterical but Harmless.", "SandwichArtist", "videodrome", "Pigpoop.jpg", 2022-10-18, 1)
INSERT INTO `Users` VALUES (null, "Nora", "Szeto", "Nora.Szeto@gmail.com", "Master of Education. Don't fuck with me.", "R2Szeto", "operation", "puppy.jpg", 2022-10-19, 1)

SELECT * FROM Tags

INSERT INTO `Categories` VALUES (null, "Health");
INSERT INTO `Categories` VALUES (null, "Sports");
INSERT INTO `Categories` VALUES (null, "Fashion");
INSERT INTO `Categories` VALUES (null, "Movies");

INSERT INTO `Posts` VALUES (null, 1, 2, "Parsnip&Pear, new cycle syncing app", 2022-10-19, "https://media-cdn.greatbritishchefs.com/media/ejzcxjnx/img18789.jpg?mode=crop&width=1536&height=1024", "Next week, a new cycle syncing app will be released by Gracie Parce, software developer. Parsnip&Pear is devoted to teaching women about their bodies and how to live more cyclically, aligned with their menstrual cycle.")
INSERT INTO `Posts` VALUES (null, 1, 2, "Parsnip&Pear, new cycle syncing app", 2022-10-19, "https://media-cdn.greatbritishchefs.com/media/ejzcxjnx/img18789.jpg?mode=crop&width=1536&height=1024", "Next week, a new cycle syncing app will be released by Gracie Parce, software developer. Parsnip&Pear is devoted to teaching women about their bodies and how to live more cyclically, aligned with their menstrual cycle.");
INSERT INTO `Posts` VALUES (null, 2, 2, "Parsnip&Pear, new cycle syncing app", 2022-10-19, "https://media-cdn.greatbritishchefs.com/media/ejzcxjnx/img18789.jpg?mode=crop&width=1536&height=1024", "Next week, a new cycle syncing app will be released by Gracie Parce, software developer. Parsnip&Pear is devoted to teaching women about their bodies and how to live more cyclically, aligned with their menstrual cycle.");

DELETE FROM Posts 
WHERE id = 3;

UPDATE Users
Set profile_image_url = "http://alexpeak.com/art/films/tta/toxie.jpg"
WHERE id = 1

UPDATE Users
Set profile_image_url = "https://news.cornell.edu/sites/default/files/styles/story_thumbnail_xlarge/public/2020-05/0505_daog1.jpg"
WHERE id = 2

