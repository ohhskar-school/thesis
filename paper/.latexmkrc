$latex = 'latex  %O  -interaction=nonstopmode --shell-escape %S';
$pdflatex = 'pdflatex  %O  -interaction=nonstopmode --shell-escape %S';

$recorder = 1;

# Ignore always-regenerated *.pyg files from the minted package when considering
# whether to run pdflatex again.
$hash_calc_ignore_pattern{'pyg'} = '.*';
