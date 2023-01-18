# Chess-Gender-Gap

## Instructions

#### Move into top-level directory
```
cd Chess-Gender-Gap

```

#### Install environment
```
conda env create -f environment.yml

```

#### Activate environment
```
conda activate chess-gender-gap

```

#### Install package
```
pip install -e src/chess-gender-gap

```

Including the optional -e flag will install the package in "editable" mode, meaning that instead of copying the files into your virtual environment, a symlink will be created to the files where they are.

#### Fetch XML data
```
python -m chess_gender_gap fetch

```

#### Run jupyter server
```
jupyter notebook notebooks/

```
You can now use the jupyter server or `chess-gender-gap` kernel to run notebooks.