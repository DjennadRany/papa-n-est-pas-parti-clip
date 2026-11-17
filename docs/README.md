# Studio Clip IA — navigateur gratuit

## Fonctions
- Import JPG/PNG multiples, MP3/WAV, titre et notes.
- Chargement direct du storyboard et de la chanson présents dans le dépôt.
- Découpage chronologique du manifeste, ajusté à la durée du MP3.
- Aperçu synchronisé, navigation par plan, zoom ou travelling.
- Export via MediaRecorder + captureStream + Web Audio, avec son.
- Export MP4 si le navigateur accepte son encodage, sinon WebM.
- Aucun upload vers un serveur. Aucune animation de personnages par IA.

## Tests
`node --test docs/studio-core.test.mjs`

## GitHub Pages
Workflow pages.yml copie docs/, scenes.json et les médias dans site/.
Le propriétaire doit activer Pages dans Settings > Pages > GitHub Actions.
Si Pages n'est pas accessible avec le dépôt privé, utiliser un hébergeur
statique gratuit compatible ou rendre le dépôt public en connaissance de
cause (ce qui rendrait aussi les images et l'audio publics).

## Limitations
MediaRecorder enregistre en temps réel; le navigateur doit rester actif.
Le MP4 n'est pas garanti: WebM est la solution de repli.
L'export audio dépend des API Web Audio/MediaRecorder du navigateur.
Le montage à base d'images est un mouvement de caméra, pas une animation
physique générée par IA. Le film de 178 s prend environ 178 s à enregistrer.
