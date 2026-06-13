/**
 * @file
 * @brief UI string translation implementation.
 *
 * Loads translation files from dat/ui/<lang>/*.txt into a map.
 * Format: English text|Spanish translation (one per line, pipe-separated).
 *
 * The pipe character (|) was chosen as separator because it:
 * - Never appears in DCSS UI strings
 * - Is visually clear
 * - Works well with grep/sed
 *
 * Lines starting with # or % are ignored (comments/section headers).
 * Blank lines are ignored.
 *
 * Format specifiers (%s, %d, @foo@) are part of the key and must match
 * exactly in the translation.
**/

#include "AppHdr.h"

#include "translation.h"

#include <cstdio>
#include <map>
#include <string>

#include "files.h"
#include "options.h"

using std::map;

// ---------------------------------------------------------------------------
// Internal state
// ---------------------------------------------------------------------------

static map<string, string> s_translations;
static bool s_initialized = false;

/**
 * The list of UI translation files to load.
 * These correspond to different categories of UI strings in the source.
 * Files are loaded in order; later files override earlier ones.
 */
static const vector<string> s_ui_files = {
    "menu.txt",
    "combat.txt",
    "status.txt",
    "skills.txt",
    "ability.txt",
    "religion.txt",
    "commands.txt",
    "inventory.txt",
    "misc.txt",
};

// ---------------------------------------------------------------------------
// File loading
// ---------------------------------------------------------------------------

/**
 * Load a single translation file into the map.
 * Format: English text|Spanish translation (pipe-separated).
 *
 * @param filepath Full path to the translation file.
 */
static void _load_translation_file(const string &filepath)
{
    FILE *fp = fopen(filepath.c_str(), "r");
    if (!fp)
        return;

    char buf[4096];
    int line_num = 0;

    while (fgets(buf, sizeof(buf), fp))
    {
        line_num++;
        string line(buf);

        // Remove trailing newline
        if (!line.empty() && line.back() == '\n')
            line.pop_back();

        // Skip comments, section headers, and blank lines
        if (line.empty() || line[0] == '#' || line[0] == '%')
            continue;

        // Find the pipe separator
        auto pipe = line.find('|');
        if (pipe == string::npos || pipe == 0 || pipe == line.length() - 1)
        {
            // Bad line - skip silently (could add debug logging later)
            continue;
        }

        string key = line.substr(0, pipe);
        string val = line.substr(pipe + 1);

        // Trim leading/trailing whitespace from value only
        // (key must match exactly, including whitespace)
        // Trim value
        size_t start = val.find_first_not_of(" \t");
        size_t end = val.find_last_not_of(" \t");
        if (start != string::npos && end != string::npos)
            val = val.substr(start, end - start + 1);

        s_translations[key] = val;
    }

    fclose(fp);
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

void init_ui_translations()
{
    if (s_initialized)
        return;

    // Don't load if no language is set (default English)
    if (!Options.lang_name || !Options.lang_name[0])
        return;

    // Try to load files from dat/ui/<lang>/
    for (const string &filename : s_ui_files)
    {
        string path = "ui/" + string(Options.lang_name) + "/" + filename;
        string full = datafile_path(path, false); // croak_on_fail = false
        if (!full.empty())
            _load_translation_file(full);
    }

    s_initialized = true;
}

void shutdown_ui_translations()
{
    s_translations.clear();
    s_initialized = false;
}

string tr(const string &english_text)
{
    if (!s_initialized || english_text.empty())
        return english_text;

    auto it = s_translations.find(english_text);
    if (it != s_translations.end())
        return it->second;

    return english_text;
}
