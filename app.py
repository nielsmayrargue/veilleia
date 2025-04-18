// Traiter la réponse du service de transcription
const response = $json;
let transcriptStatus = "missing";
let transcriptText = "";

try {
  if (response.success === true && response.transcript) {
    // Le service a renvoyé une transcription avec succès
    transcriptText = response.transcript;
    transcriptStatus = "success";
  } else if (response.error) {
    // Le service a renvoyé une erreur
    throw new Error(response.error);
  } else {
    // Réponse inattendue
    throw new Error("Format de réponse invalide");
  }
} catch (error) {
  console.log(`Erreur lors du traitement de la transcription: ${error.message}`);
  transcriptStatus = "whisper";
}

// Récupérer les données originales de la vidéo depuis le nœud précédent
const videoData = $node["Get Videos"].first().json;

// Combiner les données de la vidéo avec la transcription
return {
  json: {
    ...videoData,
    transcript: transcriptText,
    transcriptStatus: transcriptStatus
  }
};
