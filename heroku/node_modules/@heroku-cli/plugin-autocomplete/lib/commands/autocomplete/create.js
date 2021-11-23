"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs-extra");
const path = require("path");
const base_1 = require("../../base");
const debug = require('debug')('autocomplete:create');
class Create extends base_1.AutocompleteBase {
    async run() {
        this.errorIfWindows();
        // 1. ensure needed dirs
        await this.ensureDirs();
        // 2. save (generated) autocomplete files
        await this.createFiles();
    }
    async ensureDirs() {
        // ensure autocomplete cache dir
        await fs.ensureDir(this.autocompleteCacheDir);
        // ensure autocomplete completions dir
        await fs.ensureDir(this.completionsCacheDir);
    }
    async createFiles() {
        await fs.writeFile(this.bashSetupScriptPath, this.bashSetupScript);
        await fs.writeFile(this.zshSetupScriptPath, this.zshSetupScript);
        await fs.writeFile(this.bashCommandsListPath, this.bashCommandsList);
        await fs.writeFile(this.zshCompletionSettersPath, this.zshCompletionSetters);
    }
    get bashSetupScriptPath() {
        // <cacheDir>/autocomplete/bash_setup
        return path.join(this.autocompleteCacheDir, 'bash_setup');
    }
    get bashCommandsListPath() {
        // <cacheDir>/autocomplete/commands
        return path.join(this.autocompleteCacheDir, 'commands');
    }
    get zshSetupScriptPath() {
        // <cacheDir>/autocomplete/zsh_setup
        return path.join(this.autocompleteCacheDir, 'zsh_setup');
    }
    get zshCompletionSettersPath() {
        // <cacheDir>/autocomplete/commands_setters
        return path.join(this.autocompleteCacheDir, 'commands_setters');
    }
    get skipEllipsis() {
        return process.env.HEROKU_AC_ZSH_SKIP_ELLIPSIS === '1';
    }
    get commands() {
        if (this._commands)
            return this._commands;
        const plugins = this.config.plugins;
        const commands = [];
        plugins.forEach(p => {
            p.commands.forEach(c => {
                if (c.hidden)
                    return;
                try {
                    commands.push(c);
                }
                catch (error) {
                    debug(`Error creating completions for command ${c.id}`);
                    debug(error.message);
                    this.writeLogFile(error.message);
                }
            });
        });
        this._commands = commands;
        return this._commands;
    }
    get bashCommandsList() {
        return this.commands.map(c => {
            try {
                const publicFlags = this.genCmdPublicFlags(c).trim();
                return `${c.id} ${publicFlags}`;
            }
            catch (error) {
                debug(`Error creating bash completion for command ${c.id}, moving on...`);
                debug(error.message);
                this.writeLogFile(error.message);
                return '';
            }
        }).join('\n');
    }
    get zshCompletionSetters() {
        const cmdsSetter = this.zshCommandsSetter;
        const flagSetters = this.zshCommandsFlagsSetters;
        return `${cmdsSetter}\n${flagSetters}`;
    }
    get zshCommandsSetter() {
        const cmdsWithDescriptions = this.commands.map(c => {
            try {
                return this.genCmdWithDescription(c);
            }
            catch (error) {
                debug(`Error creating zsh autocomplete for command ${c.id}, moving on...`);
                debug(error.message);
                this.writeLogFile(error.message);
                return '';
            }
        });
        return this.genZshAllCmdsListSetter(cmdsWithDescriptions);
    }
    get zshCommandsFlagsSetters() {
        return this.commands.map(c => {
            try {
                return this.genZshCmdFlagsSetter(c);
            }
            catch (error) {
                debug(`Error creating zsh autocomplete for command ${c.id}, moving on...`);
                debug(error.message);
                this.writeLogFile(error.message);
                return '';
            }
        }).join('\n');
    }
    genCmdPublicFlags(Command) {
        const Flags = Command.flags || {};
        return Object.keys(Flags)
            .filter(flag => !Flags[flag].hidden)
            .map(flag => `--${flag}`)
            .join(' ');
    }
    genCmdWithDescription(Command) {
        let description = '';
        if (Command.description) {
            const text = Command.description.split('\n')[0];
            description = `:"${text}"`;
        }
        return `"${Command.id.replace(/:/g, '\\:')}"${description}`;
    }
    genZshCmdFlagsSetter(Command) {
        const id = Command.id;
        const flagscompletions = Object.keys(Command.flags || {})
            .filter(flag => Command.flags && !Command.flags[flag].hidden)
            .map(flag => {
            const f = (Command.flags && Command.flags[flag]) || { description: '' };
            const isBoolean = f.type === 'boolean';
            const hasCompletion = 'completion' in f || this.findCompletion(id, flag, f.description);
            const name = isBoolean ? flag : `${flag}=-`;
            let cachecompl = '';
            if (hasCompletion) {
                cachecompl = ': :_compadd_flag_options';
            }
            if (this.wantsLocalFiles(flag)) {
                cachecompl = ': :_files';
            }
            const help = isBoolean ? '(switch) ' : (hasCompletion ? '(autocomplete) ' : '');
            const completion = `--${name}[${help}${f.description}]${cachecompl}`;
            return `"${completion}"`;
        })
            .join('\n');
        if (flagscompletions) {
            return `_set_${id.replace(/:/g, '_')}_flags () {
_flags=(
${flagscompletions}
)
}
`;
        }
        return `# no flags for ${id}`;
    }
    genZshAllCmdsListSetter(cmdsWithDesc) {
        return `
_set_all_commands_list () {
_all_commands_list=(
${cmdsWithDesc.join('\n')}
)
}
`;
    }
    get envAnalyticsDir() {
        return `HEROKU_AC_ANALYTICS_DIR=${path.join(this.autocompleteCacheDir, 'completion_analytics')};`;
    }
    get envCommandsPath() {
        return `HEROKU_AC_COMMANDS_PATH=${path.join(this.autocompleteCacheDir, 'commands')};`;
    }
    get bashSetupScript() {
        return `${this.envAnalyticsDir}
${this.envCommandsPath}
HEROKU_AC_BASH_COMPFUNC_PATH=${path.join(__dirname, '..', '..', '..', 'autocomplete', 'bash', 'heroku.bash')} && test -f $HEROKU_AC_BASH_COMPFUNC_PATH && source $HEROKU_AC_BASH_COMPFUNC_PATH;
`;
    }
    get zshSetupScript() {
        return `${this.skipEllipsis ? '' : this.completionDotsFunc}
${this.envAnalyticsDir}
${this.envCommandsPath}
HEROKU_AC_ZSH_SETTERS_PATH=\${HEROKU_AC_COMMANDS_PATH}_setters && test -f $HEROKU_AC_ZSH_SETTERS_PATH && source $HEROKU_AC_ZSH_SETTERS_PATH;
fpath=(
${path.join(__dirname, '..', '..', '..', 'autocomplete', 'zsh')}
$fpath
);
autoload -Uz compinit;
compinit;
`;
    }
    get completionDotsFunc() {
        return `expand-or-complete-with-dots() {
  echo -n "..."
  zle expand-or-complete
  zle redisplay
}
zle -N expand-or-complete-with-dots
bindkey "^I" expand-or-complete-with-dots`;
    }
    wantsLocalFiles(flag) {
        return [
            'file',
            'procfile',
        ].includes(flag);
    }
}
exports.default = Create;
Create.hidden = true;
Create.description = 'create autocomplete setup scripts and completion functions';
