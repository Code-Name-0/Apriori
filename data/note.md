

# to avoid uploading large files, datasets will not be included in the repo
## download the original dataset from the link bellow
https://archive.ics.uci.edu/dataset/352/online+retail

## after extraxting, move the xlsx file to the data folder in the project directory
# important: name the downloaded dataset as: original.xlsx
## next run the process notebook to generate the transactions dataset

### changes made to the original dataset are:
<ol>
    <li>converted the StockCode column into string to make sure all rows have the dame dtype</li>
    <li>as this study only concerns patterns between different products, returned items will not be of importance, therefore, the removal of rows with negative quantities (returns)</li>
</ol>
