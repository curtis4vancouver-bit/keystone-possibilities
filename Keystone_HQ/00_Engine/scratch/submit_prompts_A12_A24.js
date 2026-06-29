async () => {
  const prompts = [
    { num: 12, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal her face in a close-up behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above creating a sharp shadow on one side of her face. Her eyes snap open and she looks directly into the camera lens with calm fierce intensity. She holds the stare without blinking. Her right hand reaches down to the mixer below frame. Camera holds perfectly still. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace. At 0:08, her jaw tightens almost imperceptibly. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 13, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a wide shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pushes in from wide toward medium. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Thin haze thickens slightly around her. Both her hands move across the decks with faster more confident movements. Her head bobs with building energy. The wide shot shows the full dramatic scale of the minimal booth against pure black. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she shifts her weight forward leaning into the decks. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 14, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium-close shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She pauses for a beat. Both hands rest flat on the mixer. She takes a slow deliberate breath. Camera holds steady on her face. Her expression is one of focused anticipation. Complete control. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace. At 0:08, her fingers curl slightly on the mixer edge. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 15, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She brings both hands decisively onto the controller and begins working the mixer with sharp precise movements. Camera slowly pushes in from medium to medium-close. Her head nods with authority. Her expression shifts to a subtle confident smirk. Maximum energy but complete control. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she lifts her chin slightly. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 16, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a wide shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera holds the wide shot showing the full booth and figure. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Thick haze drifts through the light beams. She is in full performance mode with her hands moving fluidly across the mixer. Her body moves with aggressive controlled energy. She owns the space. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she glances up from the decks directly at the camera. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 17, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera smoothly moves around her from left to right in a continuous slow arc. Single warm teal spotlight from directly above follows as the camera moves. Soft steady amber accent shifts as the angle changes. As the camera passes in front of her she locks eyes with the lens with a fierce composed expression. Her hands never stop moving on the decks. Cinematic and powerful. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she breaks eye contact and looks back down at the decks. At 0:09, the camera executes a rapid 1-second whip-pan continuing to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 18, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium-close shot from slightly camera-right behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left catches her profile. She leans forward slightly into the decks, one hand adjusting the high EQ while the other holds the crossfader. Her chin drops and she watches her own hands work with total focus. Camera slowly pushes in. Her gold chain hangs forward. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she tilts her head slightly to one side. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 19, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Camera holds steady. Both hands work the mixer with fluid practiced movements. She looks up from the decks and stares directly into the camera with an intense knowing smirk. She is completely in her element. Peak confidence. Camera slowly pushes in to medium-close. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she gives the slightest nod to camera. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 20, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Camera holds steady at medium distance. Her expression is calm and satisfied. Her head nods rhythmically at a steady pace. She looks down at the decks briefly then back up with a slight knowing smile. She has found her stride. Thin haze drifts gently. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she exhales visibly and her shoulders drop slightly in relaxation. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 21, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pulls back from medium to medium-wide. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Her left hand slides the crossfader while her right hand reaches across to adjust the incoming channel EQ. The movement is fluid and practiced. Professional and effortless. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she finishes the transition and both hands settle on the mixer. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 22, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She finishes a mix transition and nods once to herself in quiet approval. She rolls her shoulders once then leans back into the decks with renewed easy energy. Camera holds steady. She glances to camera-left briefly as if acknowledging someone then looks back to the decks with a half-smile. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, her gaze returns to center. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 23, text: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pulls back from medium to wide. Single warm teal spotlight from directly above begins to dim very gradually. Soft steady amber accent from camera-left softens. She makes one last smooth adjustment to the mixer and lets the track ride. She takes one hand off the controller and rests it on the edge of the booth. Her head still nods gently. The energy is winding down naturally. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, her remaining hand lifts from the mixer. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" },
    { num: 24, text: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a wide shot standing behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above is dim. Soft amber accent is barely visible. She lifts both hands off the controller and lets them rest at her sides. She looks up from the decks directly into the camera with a calm powerful stare. The teal spotlight slowly dims further. Her silhouette becomes darker and darker. She gives one final slow nod. The light fades until only the faintest outline of her face is visible against pure black. No subtitles. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face" }
  ];

  async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
  }

  async function waitFor(fn, name, timeout = 6000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const res = fn();
      if (res) return res;
      await sleep(150);
    }
    throw new Error("Timeout waiting for " + name);
  }

  const results = [];

  for (let idx = 0; idx < prompts.length; idx++) {
    const promptText = prompts[idx].text;
    const clipNum = prompts[idx].num;
    console.log(`Submitting clip A${clipNum}...`);

    try {
      // 1. Click "+ Create" button
      const plusBtn = await waitFor(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        return buttons.find(b => b.innerText && b.innerText.includes('add_2') && b.innerText.includes('Create'));
      }, "+ Create button");
      plusBtn.click();

      // 2. Click Characters tab
      const charTab = await waitFor(() => {
        const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
        return tabs.find(t => t.innerText && t.innerText.includes('Characters'));
      }, "Characters tab");
      charTab.click();

      // 3. Select Ana Stevenson card inside dialog
      const anaEl = await waitFor(() => {
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) return null;
        const elements = Array.from(dialog.querySelectorAll('*'));
        return elements.find(el => el.innerText && el.innerText.trim() === 'Ana Stevenson');
      }, "Ana Stevenson card");
      anaEl.click();

      // 4. Click Add to Prompt button
      const addBtn = await waitFor(() => {
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) return null;
        return Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Add to Prompt'));
      }, "Add to Prompt button");
      addBtn.click();

      // 5. Wait for dialog to close
      await waitFor(() => !document.querySelector('[role="dialog"]'), "dialog to close");

      // 6. Focus editor, clear and type text
      const editor = await waitFor(() => document.querySelector('div[contenteditable="true"]'), "editor");
      editor.focus();
      editor.innerText = '';
      editor.dispatchEvent(new Event('input', { bubbles: true }));
      document.execCommand('insertText', false, promptText);

      // 7. Click submit Create button
      const submitBtn = await waitFor(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const btn = btns.find(b => b.innerText && b.innerText.includes('Create') && b.innerText.includes('arrow_forward'));
        return (btn && !btn.disabled) ? btn : null;
      }, "enabled Create button");
      
      submitBtn.click();
      results.push({ clip: `A${clipNum}`, status: "Success" });
      console.log(`Successfully submitted A${clipNum}!`);

      // 8. Sleep 8 seconds before next prompt to allow queueing
      await sleep(8000);
    } catch (err) {
      console.error(`Error submitting A${clipNum}:`, err.message);
      results.push({ clip: `A${clipNum}`, status: "Failed: " + err.message });
      // If we failed, let's close the dialog if it's still open to reset the state
      const dialog = document.querySelector('[role="dialog"]');
      if (dialog) {
        const closeBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('close') || b.innerText.includes('Cancel')));
        if (closeBtn) closeBtn.click();
      }
      await sleep(3000);
    }
  }

  return results;
}
