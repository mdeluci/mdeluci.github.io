# Mario de Lucio's website

Source of my personal academic website: **[mdeluci.github.io](https://mdeluci.github.io)**

I am a computational scientist working on computational mechanics and computational fluid dynamics for
biomedical and mechanical engineering. The site collects my research, publications, CV, teaching and news.

## Structure

| Folder / file | Content |
| --- | --- |
| `_pages/` | Main pages: About, Research, Publications, CV, Teaching, Videos |
| `_news/` | News items shown on the home page |
| `_posts/` | Blog posts |
| `_projects/` | Project pages |
| `_bibliography/papers.bib` | Publications list |
| `_data/cv.yml` | CV content |
| `assets/` | Images, PDFs, videos |
| `_sass/` | Styles and color theme |

## Updating the site

Edit the files above and push to `master`. GitHub Actions builds and deploys the site automatically.

To preview locally:

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Credits

Built with Jekyll, based on the [al-folio](https://github.com/alshedivat/al-folio) theme (MIT License).
