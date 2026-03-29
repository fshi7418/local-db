#!/bin/bash
# shellcheck source=/dev/null
source ~/Environments/personal1/bin/activate
cd ~/Repos/local-db || exit

# --- Validation Functions ---
function is_valid_integer() {
    if [[ $1 =~ ^[0-9]+$ ]]; then
        return 0
    else
        return 1
    fi
}

function is_valid_date() {
    if [[ $1 =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        return 0
    else
        return 1
    fi
}

# --- Insert Book Author ---
function insert_book_author() {
    echo "Insert a new Book Author"
    read -p "First name: " first_name
    read -p "Last name (optional): " last_name
    read -p "Middle name (optional): " middle_name
    read -p "Birthday year (YYYY, optional): " birth_year
    read -p "Birthday month (MM, optional): " birth_month
    read -p "Birthday day (DD, optional): " birth_day
    read -p "Death year (YYYY, optional): " death_year
    read -p "Death month (MM, optional): " death_month
    read -p "Death day (DD, optional): " death_day
    read -p "Nationality (optional, ISO 3166-1 alpha-2 code): " nationality

    python3 script_modules/add_book_author.py "$first_name" "$last_name" "$middle_name" "$birth_year" "$birth_month" "$birth_day" "$death_year" "$death_month" "$death_day" "$nationality"
}

# --- Insert Book Publisher ---
function insert_book_publisher() {
    echo "Insert a new Book Publisher"
    read -p "Publisher name: " publisher_name

    python3 script_modules/add_book_publisher.py "$publisher_name"
}

function insert_book_series() {
    echo "Insert a new Book Series"
    read -p "Series name: " series_name
    read -p "Number of books: " num_books
    echo -----
    python3 utilities.py function display_book_publishers
    read -p "Enter Book Publisher ID: " publisher_id

    python3 script_modules/add_book_series.py "$series_name" "$num_books" "$publisher_id"
}

# --- Insert Book Translator ---
function insert_book_translator() {
    echo "Insert a new Book Translator"
    read -p "First name: " first_name
    read -p "Last name: " last_name
    read -p "Middle name (optional): " middle_name

    python3 script_modules/add_book_translator.py "$first_name" "$last_name" "$middle_name"
}

# --- Insert Book Editor ---
function insert_book_editor() {
    echo "Insert a new Book Editor"
    read -p "First name: " first_name
    read -p "Last name (optional): " last_name
    read -p "Middle name (optional): " middle_name

    python3 script_modules/add_book_editor.py "$first_name" "$last_name" "$middle_name"
}

# --- Insert Book ---
function insert_book() {
    echo "Insert a new Book"

    # Show current publishers, authors, translators, languages, series, formats
    echo "Choose a Publisher:"
    python3 utilities.py function display_book_publishers
    read -p "Publisher ID: " publisher_id

    echo "Choose authors (comma separated for multiple):"
    python3 utilities.py function display_book_authors
    read -p "Author IDs (comma separated for multiple): " author_ids

    echo "Choose translators (optional):"
    python3 utilities.py function display_book_translators
    read -p "Translator IDs (comma separated, optional): " translator_ids

    echo "Choose editors (comma separated for multiple):"
    python3 utilities.py function display_book_editors
    read -p "Editor IDs (comma separated for multiple): " editor_ids

    echo "Choose languages (comma separated for multiple):"
    python3 utilities.py function display_book_language
    read -p "Language IDs (comma separated for multiple): " language_ids

    echo "Choose a Series (optional):"
    python3 utilities.py function display_book_series
    read -p "Series ID (or leave blank): " series_id

    read -p "Series order (optional): " series_order

    echo "Choose a Format:"
    python3 utilities.py function display_book_format
    read -p "Format ID: " format_id

    read -p "Title: " title
    read -p "Subtitle (optional): " subtitle
    read -p "ISBN (optional): " isbn
    read -p "ISBN13 (optional): " isbn13
    read -p "Publication year (YYYY), optional): " publication_year
    read -p "Publication month (MM, optional): " publication_month
    read -p "Publication day (DD, optional): " publication_day
    read -p "Edition (optional): " edition
    read -p "Page count (optional): " page_count
    read -p "Date read (YYYY-MM-DD, optional): " date_read

    python3 script_modules/add_book.py \
        "$title" "$subtitle" "$isbn" "$isbn13" "$publication_year" "$publication_month" "$publication_day" \
        "$page_count" "$date_read" "$series_order" "$publisher_id" "$series_id" "$format_id" "$author_ids" \
        "$language_ids" "$translator_ids" "$editor_ids" "$edition"
}

# --- Main Menu ---
echo "Book Database CLI"
echo "1) Insert Book Author"
echo "2) Insert Book Publisher"
echo "3) Insert Book Translator"
echo "4) Insert Book"
echo "5) Insert Book Editor"
echo "6) Insert Book Series"
read -p "Choose an option: " option

case $option in
    1) insert_book_author ;;
    2) insert_book_publisher ;;
    3) insert_book_translator ;;
    4) insert_book ;;
    5) insert_book_editor ;;
    6) insert_book_series ;;
    *) echo "Invalid option" ;;
esac
