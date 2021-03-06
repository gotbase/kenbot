# kenbot Docs
This is the kenbot documentation which is deployed on [docs.kenbot.online](https://docs.kenbot.online/).

It uses [Sphinx](https://www.sphinx-doc.org/en/master/) to generate the website which is automatically re-deployed 
upon each merge on `dev` branch.

## Build this doc
To locally build this doc, first install Sphinx and the necessary requirements.
```bash
$ python3 -m pip -r doc_requirements.txt -r requirements.txt
```

Then go to the `docs` directory and run (depending on your os).
```bash
$ make html
```
```bash
$ make.bat html
```

The documentation website is now available at `docs/build/html/index.html`.

## Contribute
To contribute to this documentation, please open a pull request to merge your contribution branch on `dev`.

## Images
Images are stored on the `assets` branch of this repository. To add an image to this documentation, add it to the 
`assets` branch (via pull request) and reference it directly from this doc.

Example with `assets/wiki_resources/kenbot_arch.svg` stored at [kenbot/assets/wiki_resources/kenbot_arch.svg](https://github.com/gotbase/kenbot/blob/assets/wiki_resources/kenbot_arch.svg):
```rst
.. image:: https://raw.githubusercontent.com/gotbase/kenbot/assets/wiki_resources/kenbot_arch.svg
   :target: https://raw.githubusercontent.com/gotbase/kenbot/assets/wiki_resources/kenbot_arch.svg
   :alt: kenbot architecture
```
