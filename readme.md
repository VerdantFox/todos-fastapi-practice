# Simple Tailwind CSS Starter

This is an extremley simple setup to develop Tailwind projects. This will be used in my Tailwind From Scratch course.

## Usage

Install dependencies

```bash
npm install
```

Run Tailwind CLI in watch mode

```bash
npm run dev
```

You can use tailwind classes in any .html files in the root directory

Put any custom CSS that you may have in the **src/input.css** file

Add any config values to the **tailwind.config.js** file

To build once, run

```bash
npm run build
```

You only need to deploy your html files and css/style.css

## BROWSER SYNC

Reload server on ".py", ".css", ".js" file changes with the following command:

```bash
uvicorn web.main:app --reload --reload-include="*.html" --reload-include="*.css" --reload-include="*.js"
```

In a separate terminal, hot-reload a proxy server to localhost:800 with:

```bash
browser-sync 'http://localhost:8000' 'web/html/static' -w -f .
```
