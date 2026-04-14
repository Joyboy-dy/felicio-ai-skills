#!/usr/bin/env node

const { Command } = require('commander');
const chalk = require('chalk');
const fs = require('fs-extra');
const path = require('path');
const fetch = require('node-fetch');
const os = require('os');
const readline = require('readline');

const program = new Command();
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/Joyboy-dy/felicio-ai-skills/main/';
const MANIFEST_URL = `${GITHUB_RAW_BASE}skills.manifest.json`;
const GLOBAL_DIR = path.join(os.homedir(), '.felicio-ai-skills');

async function askQuestion(query) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise(resolve => rl.question(query, ans => {
    rl.close();
    resolve(ans);
  }));
}

async function fetchManifest() {
  try {
    const response = await fetch(MANIFEST_URL);
    if (!response.ok) throw new Error(`Impossible de récupérer le manifeste: ${response.statusText}`);
    return await response.json();
  } catch (error) {
    console.error(chalk.red('Error:'), error.message);
    process.exit(1);
  }
}

async function downloadFile(relativeRepoPath, targetBaseDir) {
  const url = `${GITHUB_RAW_BASE}${relativeRepoPath}`;
  
  // Nettoyer le chemin pour l'installation
  let relativePath = relativeRepoPath
    .replace('skills/felicio-ai-toolkit/', '')
    .replace('skills/from-skills.sh/', '');
  
  const destPath = path.join(targetBaseDir, relativePath);

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Erreur de téléchargement ${url}: ${response.statusText}`);
    
    const content = await response.text();
    await fs.ensureDir(path.dirname(destPath));
    await fs.writeFile(destPath, content);
    console.log(`${chalk.green('✔')} Installé: ${path.relative(process.cwd(), destPath) || destPath}`);
  } catch (error) {
    console.error(chalk.red('✘ Error downloading'), relativeRepoPath, ':', error.message);
  }
}

program
  .name('felicio-ai-skills')
  .description('CLI pour installer les skills Felicio AI')
  .version('1.1.0');

program
  .command('list')
  .description('Liste tous les skills disponibles')
  .action(async () => {
    const manifest = await fetchManifest();
    console.log(chalk.cyan.bold('\nSkills disponibles :\n'));
    manifest.skills.forEach(skill => {
      console.log(`${chalk.yellow.bold(skill.name)}: ${skill.description}`);
    });
    console.log();
  });

program
  .command('init')
  .description('Installe les skills localement ou globalement')
  .option('-g, --global', 'Installe les skills globalement dans ~/.felicio-ai-skills/')
  .action(async (options) => {
    const targetDir = options.global ? GLOBAL_DIR : path.join(process.cwd(), '.claude', 'skills');
    
    if (options.global && await fs.exists(GLOBAL_DIR)) {
      const answer = await askQuestion(chalk.yellow(`~/.felicio-ai-skills already exists. Update? (y/n): `));
      if (answer.toLowerCase() !== 'y') {
        console.log(chalk.blue('Operation cancelled.'));
        return;
      }
    }

    const manifest = await fetchManifest();
    console.log(chalk.cyan.bold(`\nInitialisation des skills ${options.global ? 'globalement' : 'localement'}...\n`));
    
    for (const skill of manifest.skills) {
      for (const file of skill.files) {
        await downloadFile(file, targetDir);
      }
    }

    if (options.global) {
      console.log(chalk.green.bold('\n✓ Skills installed globally in ~/.felicio-ai-skills/'));
      console.log(chalk.blue('→ Run "npx @joyboy-dy/felicio-ai-skills link" in any project to use them.\n'));
    } else {
      console.log(chalk.green.bold('\n✨ Tous les skills ont été installés localement avec succès !\n'));
    }
  });

program
  .command('add <skill-name>')
  .description('Installe un skill spécifique localement')
  .action(async (skillName) => {
    const manifest = await fetchManifest();
    const skill = manifest.skills.find(s => s.name === skillName);
    
    if (!skill) {
      console.error(chalk.red(`\nSkill "${skillName}" non trouvé.`));
      console.log('Utilisez `list` pour voir les skills disponibles.\n');
      return;
    }

    const targetDir = path.join(process.cwd(), '.claude', 'skills');
    console.log(chalk.cyan.bold(`\nInstallation du skill: ${skillName}...\n`));
    for (const file of skill.files) {
      await downloadFile(file, targetDir);
    }
    console.log(chalk.green.bold(`\n✨ Skill "${skillName}" installé avec succès !\n`));
  });

program
  .command('link')
  .description('Lien symbolique des skills globaux vers le projet courant')
  .option('-d, --dir <directory>', 'Dossier de destination (défaut: .claude/skills)', '.claude/skills')
  .action(async (options) => {
    if (!(await fs.exists(GLOBAL_DIR))) {
      console.log(chalk.red('No global skills found. Run "init --global" first.'));
      return;
    }

    const targetDir = path.resolve(process.cwd(), options.dir);

    if (await fs.exists(targetDir)) {
      console.log(chalk.yellow('Already linked or directory exists.'));
      return;
    }

    try {
      await fs.ensureDir(path.dirname(targetDir));
      // Utiliser 'junction' sur Windows pour les dossiers, 'dir' ou 'file' ailleurs
      const type = os.platform() === 'win32' ? 'junction' : 'dir';
      await fs.symlink(GLOBAL_DIR, targetDir, type);
      console.log(chalk.green.bold(`\n✓ Linked ${GLOBAL_DIR} → ${path.relative(process.cwd(), targetDir)}\n`));
    } catch (error) {
      console.error(chalk.red('Error creating symlink:'), error.message);
    }
  });

program
  .command('unlink')
  .description('Supprime le lien symbolique du projet courant')
  .option('-d, --dir <directory>', 'Dossier du lien (défaut: .claude/skills)', '.claude/skills')
  .action(async (options) => {
    const targetDir = path.resolve(process.cwd(), options.dir);

    if (!(await fs.exists(targetDir))) {
      console.log(chalk.yellow('No link found to remove.'));
      return;
    }

    try {
      const stats = await fs.lstat(targetDir);
      if (stats.isSymbolicLink()) {
        await fs.unlink(targetDir);
        console.log(chalk.green('\n✓ Link removed.\n'));
      } else {
        console.log(chalk.red('The specified directory is not a symbolic link.'));
      }
    } catch (error) {
      console.error(chalk.red('Error removing link:'), error.message);
    }
  });

program.parse(process.argv);
