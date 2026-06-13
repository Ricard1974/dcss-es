/**
 * @file
 * @brief UI string translation system for DCSS.
 *
 * Provides a simple key-value translation system for hardcoded C++ UI strings.
 * Translations are loaded from dat/ui/<lang>/*.txt files at startup.
 * Falls back to English if no translation is found.
 *
 * Usage:
 *   mpr(tr("You die..."));
 *   mprf(tr("You hit %s."), mon.name().c_str());
 *
 * File format (dat/ui/es/menu.txt):
 *   # Comments
 *   English text|Spanish translation
 *   You die...|Has muerto...
**/

#pragma once

#include <string>
#include <vector>

using std::string;
using std::vector;

/**
 * Initialize the UI translation system.
 * Loads translation files from dat/ui/<lang>/ directory.
 * Must be called after Options.lang_name is set.
 */
void init_ui_translations();

/**
 * Shutdown the UI translation system.
 * Frees all loaded translations.
 */
void shutdown_ui_translations();

/**
 * Translate a UI string from English to the current language.
 * @param english_text The English text to translate.
 * @returns The translated text, or the original English text if no
 *          translation is found. Format specifiers (%s, %d, etc.)
 *          are preserved in the translation.
 */
string tr(const string &english_text);
