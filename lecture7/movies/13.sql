SELECT DISTINCT peeps.name
FROM people AS kb
         JOIN stars AS ks ON kb.id = ks.person_id
         JOIN stars AS os ON ks.movie_id = os.movie_id
         JOIN people AS peeps ON os.person_id = peeps.id
WHERE peeps.id != kb.id
  AND kb.birth = 1958
  AND kb.name = 'Kevin Bacon';
