# Myanmar Handwriting Dataset Project

This repository is an Assignment 3 project for **Sir. Ye Kyaw Thu's AIE class**. The project focuses on building a small end-to-end workflow for **collecting, organizing, and preparing a handwritten Myanmar syllable dataset**. It includes a web-based data collection interface, supporting desktop tools, and a conversion script for turning recorded stroke files into image data for later experimentation in handwriting recognition, dataset analysis, or machine learning tasks.

The main goal of the project is to make Myanmar handwritten data collection more structured and reusable. Writers can create user profiles, draw Myanmar syllables with a stylus, save stroke-based samples, and organize those samples in a consistent per-user dataset format.

## Project Overview

This project provides:

- A **Flask web application** for collecting handwritten Myanmar syllable data
- A browser-based drawing interface designed for stylus input on tablets such as iPad
- Automatic organization of samples by writer
- Progress tracking for dataset collection
- Utilities to browse saved stroke data
- A conversion script to transform stroke files into image files

The repository currently uses a syllable list from `syl.txt` and stores handwritten samples as stroke coordinates inside the `dataset/` directory.

## Course Context

This work was prepared as part of **Assignment 3** for **Sir. Ye Kyaw Thu's AIE class**. The project demonstrates how to:

- design a dataset collection workflow,
- build a simple annotation or handwriting capture interface,
- store raw handwriting data in a reusable format, and
- prepare collected samples for future image-based or sequence-based processing.

## Dataset Link

Dataset download link:

`[https://1drv.ms/f/c/d705d75cc7a637c7/IgD9QEaTkD0ORIUzAzTorRgIAcIrmQ8O8Uhd0PUQI899vbcAdd your OneDrive dataset link here]`

You can replace the placeholder above with your public or shared OneDrive link when you are ready.

## Main Features

- **Writer management**
  Create and manage writers with metadata such as name, age, sex, and education.

- **Myanmar syllable presentation**
  Load syllables from `syl.txt` and show them one by one for writing.

- **Stroke capture**
  Save handwriting as stroke sequences with `(x, y, timestamp)` values.

- **Progress tracking**
  Track how many syllables each user has completed and resume from the next unfinished item.

- **Multiple samples per syllable**
  Save repeated samples for the same syllable using file names such as `1-1.txt`, `1-2.txt`, and `1-3.txt`.

- **Dataset visualization and conversion**
  Inspect samples with the browser tool and convert stroke data into images using `convert2image.py`.

## Technologies Used

- Python
- Flask
- Werkzeug
- HTML, CSS, JavaScript
- Pillow
- PyQt5 utilities for desktop collection and browsing

## Project Structure

```text
Myanmar-HandWritting-Dataset-Project/
|-- app.py
|-- convert2image.py
|-- dataset_browser.py
|-- hw_collector.py
|-- requirements.txt
|-- syl.txt
|-- Assignment_3.pdf
|-- templates/
|   `-- index.html
`-- dataset/
    `-- <writer_name>/
        |-- user_info.json
        |-- 1-1.txt
        |-- 1-2.txt
        `-- ...
```

## Dataset Format

Each writer has a separate folder inside `dataset/`. A typical writer folder contains:

- `user_info.json` for writer information
- stroke files such as `1-1.txt`, `25-2.txt`, or `300-3.txt`

### File naming convention

`<syllable_index>-<sample_number>.txt`

Example:

- `1-1.txt` = first sample of syllable 1
- `1-2.txt` = second sample of syllable 1
- `50-3.txt` = third sample of syllable 50

### Stroke file format

Each stroke file stores handwriting as a sequence of strokes:

```text
STROKE 1
x y timestamp
x y timestamp

STROKE 2
x y timestamp
x y timestamp
```

This preserves the order of writing and supports both stroke-based processing and image conversion.

## Current Repository Snapshot

Based on the current repository contents:

- `syl.txt` contains **4,413** Myanmar syllable entries
- the `dataset/` folder currently contains **1 writer folder**
- the repository currently includes **13,343 stroke sample files**

These numbers may grow as more writers and samples are added.

## Web Application

The main data collection app is implemented in `app.py` and `templates/index.html`.

### What the web app does

- loads Myanmar syllables from `syl.txt`
- lets the user create or select a writer
- shows one syllable at a time
- captures stylus-based handwriting on a canvas
- saves stroke data into the appropriate writer folder
- keeps track of completed syllables and resume position

### API endpoints

The Flask app includes endpoints such as:

- `GET /api/users`
- `POST /api/users`
- `GET /api/users/<user_name>`
- `GET /api/syllables`
- `GET /api/syllables/<index>`
- `POST /api/save-strokes`
- `GET /api/get-user-progress`

## Other Scripts

### `convert2image.py`

This script converts stroke-based handwriting files into image files. It supports:

- output image size selection,
- `png` or `jpg` format,
- single-color drawing,
- per-stroke random colors, and
- time-based coloring.

Example:

```bash
python convert2image.py --dataset dataset --output output
```

### `dataset_browser.py`

A PyQt-based utility for browsing writers, stroke files, and the associated Myanmar syllable labels.

### `hw_collector.py`

A desktop PyQt handwriting collector that provides a GUI alternative to the web collector.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Myanmar-HandWritting-Dataset-Project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install pillow pyqt5
```

## How to Run

### Run the Flask web collector

```bash
python app.py
```

The server starts on:

```text
http://localhost:5001
```

If you are using a tablet on the same local network, you can also access the app from the host machine's local IP address.

### Run the desktop collector

```bash
python hw_collector.py --file syl.txt
```

### Run the dataset browser

```bash
python dataset_browser.py --dataset dataset --textfile syl.txt
```

### Convert stroke files to images

```bash
python convert2image.py --dataset dataset --output output
```

## Why This Project Matters

Myanmar handwriting resources are relatively limited compared with datasets available for many other languages. This project is useful because it helps:

- collect raw handwriting data in a structured format,
- preserve stroke order and timing information,
- support future handwriting recognition research,
- create image-based training data from the same raw files, and
- encourage practical dataset-building work in an academic setting.

## Future Improvements

- Add export tools for CSV or JSON summaries
- Support direct cloud backup for collected samples
- Add better writer statistics and quality checks
- Improve mobile responsiveness further
- Extend metadata collection for research use
- Add train, validation, and test split generation scripts

## Acknowledgment

This project was created for **Sir. Ye Kyaw Thu's AIE class** as part of **Assignment 3**. It is intended as an academic project for Myanmar handwriting dataset collection and preparation.
