
## try

    fabric /u {url} --pattern {pattern} /o {output_filename} -g=de
    RemoveLines.ps1 -FilePath "{output_filename}"

    fabric /u https://www.nosalty.hu/recept/falusi-almas-pite --pattern create_githubio_post /o current-draft-post.md -g=de
    RemoveLines.ps1 -FilePath "current-draft-post.md"

    