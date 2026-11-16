# Papa n'est pas parti — clip animé

Projet privé : montage de la chanson originale sur 24 scènes illustrées.

## Statut
Étape 2 — moteur **Remotion + React** installé dans ce dépôt. Les 24 fichiers JPEG et le MP3 doivent encore être ajoutés au dépôt.

## Organisation
- `src/Clip.jsx` : animation 2D, mouvements de caméra, ambiances et effets par scène
- `src/Root.jsx` : composition 1920 × 1080, 24 fps, 177,984 secondes
- `scenes.json` : les 24 plans et leurs timecodes
- `public/assets/images/01.jpg` à `24.jpg` : images du storyboard **à importer**
- `public/assets/audio/song.mp3` : chanson **à importer**
- `.github/workflows/render.yml` : rendu cloud déclenché manuellement (ne s'exécute jamais automatiquement)

## Importer les médias
Télécharger et décompresser `Papa_n_est_pas_parti_projet_Git_etape1.zip` fourni dans le chat.

Déposer ses 24 JPG dans `public/assets/images/` et `song.mp3` dans `public/assets/audio/`.
Ne pas déposer le MP3 à la racine. Le storyboard PDF peut rester local pour éviter d'alourdir Git.

**Dans GitHub** : ouvrir `public/assets/images`, Add file > Upload files, glisser les 24 images, puis Commit changes. Refaire l'opération pour `public/assets/audio/song.mp3`.

## Commandes locales (Node.js 20+)
```bash
npm install
npm run studio
npm run render:preview
npm run render
```
Le rendu principal est `out/papa-n-est-pas-parti.mp4`. Le rendu léger est `out/apercu.mp4`.

## Rendu sans installation locale
Dans GitHub, onglet **Actions** > **Rendu du clip** > **Run workflow**. Attendre la fin, puis télécharger l'artifact **clip-mp4**.

Lancer un rendu consomme des minutes GitHub Actions, en particulier sur un dépôt privé ; vérifier son quota gratuit.

**Limite artistique** : cette première version anime les illustrations et les effets 2D. Elle ne génère pas encore les mouvements articulés des personnages. Les plans du dragon peuvent ensuite être remplacés par des séquences IA validées.

**Confidentialité** : conserver le dépôt privé, la chanson et les illustrations ne doivent pas être rendues publiques sans autorisation.
