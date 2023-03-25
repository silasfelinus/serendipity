document.addEventListener('DOMContentLoaded', function() {
    const avatars = document.querySelectorAll('.avatar');
  
    function changeEmotion(avatar, emotion) {
      // Replace this with your own logic for changing the avatar image based on the emotion
      const newAvatarSrc = `avatar_${emotion}.png`;
      avatar.setAttribute('src', newAvatarSrc);
    }
  
    function handleAvatarClick(event) {
      const avatar = event.target;
      // Replace 'happy' with the emotion you want to trigger
      changeEmotion(avatar, 'happy');
    }
  
    avatars.forEach(avatar => avatar.addEventListener('click', handleAvatarClick));
  });
  