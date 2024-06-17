SELECT movies.title
FROM movies
         JOIN stars AS sb ON movies.id = sb.movie_id
         JOIN stars AS sj ON movies.id = sj.movie_id
         JOIN people AS pb ON sb.person_id = pb.id
         JOIN people AS pj ON sj.person_id = pj.id
WHERE pb.name = 'Bradley Cooper'
  AND pj.name = 'Jennifer Lawrence';
