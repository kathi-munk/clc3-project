<?php

echo "Starting to load content and write it to file\n";

$file = "insertDB.sql";
$key = "8c228ae8a72426d26b29aac475d84858";

//category
$content = "INSERT INTO category VALUES (1, 'Cinema');\n";
$content .= "INSERT INTO category VALUES (2, 'Series');\n";


//movies and there videos
$movieQueries = array("Avengers" => 4, "Iron+Man" => 3, "Captain+America" => 3, "Thor" => 4,
    "Ant-Man" => 3, "Guardians+of+the+Galaxy" => 3, "Black+Panther" => 2, "The+Incredible+Hulk" => 1,
    "Doctor+Strange" => 1);

foreach ($movieQueries as $movieName => $movieCount) {
    $response = file_get_contents("https://api.themoviedb.org/3/search/movie?api_key=$key&query=$movieName");
    $jsonObject = json_decode($response, true);
    $counter = 0;
    foreach ($jsonObject["results"] as $result) {
        //movie
        $movieId = $result["id"];
        $title = $result["original_title"];
        $overview = $result["overview"];
        $date = $result["release_date"];
        $imgPath = $result["poster_path"];

        $title = str_replace("'", "", $title);
        $overview = str_replace("'", "", $overview);

        $content .= "INSERT INTO movie (id, categoryId, title, overview, release_date, imgPath) VALUES (" .
            $movieId . ", 1, '" . $title . "', '" . $overview . "', '" . $date . "', 'https://image.tmdb.org/t/p/w500" . $imgPath . "');\n";

        $counter++;

        //video
        addVideo($key, $movieId, "movie", $content);

        if ($counter == $movieCount) {
            break;
        }
    }
}

//shows
$showQueries = array("Marvel" => 4, "WandaVision" => 1);

foreach ($showQueries as $showName => $showCount) {
    $response = file_get_contents("https://api.themoviedb.org/3/search/tv?api_key=$key&query=$showName&first_air_date_year=2021");
    $jsonObject = json_decode($response, true);
    $counter = 0;
    foreach ($jsonObject["results"] as $result) {
        $movieId = $result["id"];
        $title = $result["original_name"];
        $overview = $result["overview"];
        $date = $result["first_air_date"];
        $imgPath = $result["poster_path"];

        $title = str_replace("'", "", $title);
        $overview = str_replace("'", "", $overview);

        $content .= "INSERT INTO movie (id, categoryId, title, overview, release_date, imgPath) VALUES (" .
            $movieId . ", 2, '" . $title . "', '" . $overview . "', '" . $date . "', 'https://image.tmdb.org/t/p/w500" . $imgPath . "');\n";

        $counter++;

        //video
        addVideo($key, $movieId, "tv", $content);

        if ($counter == $showCount) {
            break;
        }
    }
}

//write to file
file_put_contents($file, $content);

echo "Successfully content written to " . $file;
?>

<?php function addVideo(string $key, int $movieId, string $movieOrTv, string &$content): void
{
    $responseVideo = file_get_contents("https://api.themoviedb.org/3/$movieOrTv/$movieId/videos?api_key=$key");
    $jsonVideo = json_decode($responseVideo, true);
    foreach ($jsonVideo["results"] as $video) {
        if ($video["type"] == "Trailer" || $video["type"] == "Teaser") {
            $name = $video["name"];
            $path = "https://www.youtube.com/embed/" . $video["key"];
            $type = $video["type"];

            $name = str_replace("'", "", $name);

            $content .= "INSERT INTO video (movieId, name, path, type) VALUES (" .
                $movieId . ", '" . $name . "', '" . $path . "', '" . $type . "');\n";
        }
    }
}
?>