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

## Production vidéo IA (réelle, avec mouvements des personnages)

Le moteur Wan via `ai/generate.py` est distinct des effets de caméra du navigateur.
Chaque scène possède une consigne de jeu dans `ai/scene_prompts.json`.
Le workflow `film-ai.yml` génère au plus un plan par lancement programmé,
reprend les plans précédents depuis les artifacts, et s'arrête lorsque le quota
gratuit est épuisé. Ce n'est PAS une garantie de GPU gratuit illimité.

### Procédure reproductible
1. Vérifier les tests `Studio CPU checks` et `Validate AI film pipeline`.
2. Dans GitHub Actions, ouvrir `Produce and assemble AI film (resumable)`,
   puis `Run workflow` (1 plan recommandé).
3. Télécharger les MP4 générés dans l'artifact
   `papa-clean-ai-checkpoint-v2`; les noms sont `01.mp4` à `48.mp4`.
4. Dans Studio, charger le storyboard, puis importer les MP4. Les vignettes
   indiquent les plans IA réellement présents.
5. Le mode « Film IA uniquement » interdit le rendu si un plan manque.
   Le mode « Prévisualisation » peut afficher des images fixes mais ne
   constitue pas un film IA terminé.
6. Le montage Remotion de GitHub Actions ne démarre que si les 48 MP4
   sont disponibles et validés.

### Publication et limites
GitHub Pages échoue actuellement à `actions/configure-pages` car le site
Pages n'est pas activé ou n'est pas disponible pour ce dépôt privé.
Le workflow sauvegarde donc également `studio-static-website`, archive
statique téléchargeable. L'ouverture locale peut nécessiter un serveur HTTP
local (modules ES et chargement de JSON).
Le studio est sans frais de licence; le calcul vidéo Wan dépend d'un GPU
externe soumis à quota, ou d'un GPU local. Aucun service gratuit ne garantit
un calcul illimité. La vérification visuelle de la qualité des 48 clips reste
indispensable. Le rendu MediaRecorder est dépendant du navigateur.
