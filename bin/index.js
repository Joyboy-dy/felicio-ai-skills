#!/usr/bin/env node

const { Command } = require('commander');
const chalk = require('chalk');
const fs = require('fs-extra');
const path = require('path');
const fetch = require('node-fetch');

const program = new Command();
const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/Joyboy-dy/felicio-ai-skills/main/';
const MANIFEST_URL = `${GITHUB_RAW_BASE}skills.manifest.json`;

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

async function downloadFile(relativeRepoPath) {
  const url = `${GITHUB_RAW_BASE}${relativeRepoPath}`;
  const localPath = path.join(process.cwd(), '.claude', 'skills', relativeRepoPath.split('/').pop());
  
  // Custom logic: user wants files in .claude/skills/
  // But some skills have references/ subfolders. 
  // Should we preserve structure or flatten? 
  // Usually skills in Claude are flattened in .claude/skills/ but referenced by relative paths if needed.
  // Re-reading user request: "installe tous les skills dans .claude/skills/ du projet courant"
  
  // Let's preserve the skill's file name but if there are subfolders, maybe flatten them for simplicity in .claude/skills/ 
  // unless SKILL.md expects them in subfolders.
  // Let's create subfolders if needed to be safe.
  
  // Supprimer les dossiers parents pour l'installation locale
  let relativePath = relativeRepoPath
    .replace('felicio-ai-toolkit/', '')
    .replace('from-skills.sh/', '');
  
  const destPath = path.join(process.cwd(), '.claude', 'skills', relativePath);

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Erreur de téléchargement ${url}: ${response.statusText}`);
    
    const content = await response.text();
    await fs.ensureDir(path.dirname(destPath));
    await fs.writeFile(destPath, content);
    console.log(`${chalk.green('✔')} Installé: ${destPath.replace(process.cwd() + path.sep, '')}`);
  } catch (error) {
    console.error(chalk.red('✘ Error downloading'), relativeRepoPath, ':', error.message);
  }
}

program
  .name('felicio-ai-skills')
  .description('CLI pour installer les skills Felicio AI')
  .version('1.0.0');

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
  .description('Installe tous les skills dans .claude/skills/')
  .action(async () => {
    const manifest = await fetchManifest();
    console.log(chalk.cyan.bold('\nInitialisation des skills...\n'));
    
    for (const skill of manifest.skills) {
      for (const file of skill.files) {
        await downloadFile(file);
      }
    }
    console.log(chalk.green.bold('\n✨ Tous les skills ont été installés avec succès !\n'));
  });

program
  .command('add <skill-name>')
  .description('Installe un skill spécifique')
  .action(async (skillName) => {
    const manifest = await fetchManifest();
    const skill = manifest.skills.find(s => s.name === skillName);
    
    if (!skill) {
      console.error(chalk.red(`\nSkill "${skillName}" non trouvé.`));
      console.log('Utilisez `list` pour voir les skills disponibles.\n');
      return;
    }

    console.log(chalk.cyan.bold(`\nInstallation du skill: ${skillName}...\n`));
    for (const file of skill.files) {
      await downloadFile(file);
    }
    console.log(chalk.green.bold(`\n✨ Skill "${skillName}" installé avec succès !\n`));
  });

program.parse(process.argv);
