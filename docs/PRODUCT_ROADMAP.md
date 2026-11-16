# Studio Clip IA — Audit DSI et Kanban

## Vision
48 images + scénario + chanson -> 48 vidéos animées -> MP4 final synchronisé.
Pas de diaporama déguisé. Pas de rendu final si un plan manque.

## Audit confirmé
P0: GitHub Pages refuse le déploiement (403 permissions/forfait).
P0: ZeroGPU limite le nombre de générations. GitHub Actions n'offre pas de GPU de génération.
P0: les images 25–48 contiennent des cartouches filename. Prétraitement obligatoire.
P0: le statut «Success» d'un workflow signifie checkpoint réussi, pas film terminé.
P1: vitesse vidéo fixée à 3,5 secondes par plan malgré durées différentes.
P1: sauvegarde MP4 en artifacts expirables.
P1: pas d'authentification backend pour importer depuis GitHub Pages privé.
P1: pas de détection du rythme ni de contrôle automatique de continuité.

## Architecture cible
UI: importer images/audio/storyboard, tableau Kanban, lecture/validation, export.
API authentifiée: projets, scènes, fichiers, jobs, états, coût, exports.
Queue persistante: retries bornés, idempotence par hash image+prompt+modèle,
leases et checkpoints, erreurs explicites, approbation humaine.
Providers: Wan Hugging Face existant; ComfyUI local/remote via /prompt,
/history et /view; MiniMax H3 via API officielle et clé serveur; LTX via
workflow ComfyUI. Chaque provider retourne un MP4 et métadonnées.
Stockage durable: object storage (pas seulement GitHub Actions artifacts).
QC: ffprobe, durée, résolution, absence de cartouches, identité personnages.
Montage: Remotion + FFmpeg, audio original, coupes sur frames.

## Kanban
### Done — implémenté, pas nécessairement validé E2E
- [x] Manifeste 48 plans
- [x] Générateur Wan HF
- [x] Checkpoints GitHub Actions
- [x] Prétraitement images 25–48
- [x] Tests chronologie et sources
- [x] Montage bloquant si plans manquants
### In progress
- [ ] Vérifier workflow et restauration réelle entre runs
- [ ] Inspecter visuellement nettoyage des cartouches
- [ ] Déployer GitHub Pages ou hébergement alternatif
- [ ] Corriger gestion de durée variable
### Backlog prioritaire
- [ ] Authentification et uploads depuis UI
- [ ] Adapter MiniMax H3 API avec tests mockés et gestion de coût
- [ ] Adapter ComfyUI Wan/LTX et validation workflows JSON
- [ ] Queue persistante et workers
- [ ] Stockage objet durable et signatures de fichiers
- [ ] Synchronisation musique/paroles/rythme
- [ ] Contrôle qualité de mouvement et identité
- [ ] Tests E2E 48 scènes, film complet, audio intact

## Definition of Done
48 MP4 réellement animés, chacun validé, film final lisible avec chanson,
rapport automatique et interface de production opérationnelle.
Aucune promesse d'exécution sans capacité GPU ou budget fournisseur.
