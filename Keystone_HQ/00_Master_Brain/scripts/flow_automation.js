(() => {
    const clips = [
        {
            "id": "A1",
            "speaker": "He",
            "text": "You know you are getting older when just bending over to tie your shoes feels like an absolute Olympic sport. But what if it didn't?",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Camera slowly zooms in. He speaks bluntly, hands moving naturally. No subtitles."
        },
        {
            "id": "A2",
            "speaker": "He",
            "text": "What if the creaks and the joint pain were just a lack of raw materials? I am sitting at two hundred ten pounds right now.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, slight 20-degree rotation. Builder persona, hands emphasizing points. No subtitles."
        },
        {
            "id": "A3",
            "speaker": "She",
            "text": "That is an amazing personal case study. But just a reminder to everyone watching, we are not doctors and this is certainly not medical advice.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Professional posture, camera zooms out slightly. Speaking clearly. No subtitles."
        },
        {
            "id": "A4",
            "speaker": "She",
            "text": "Always consult your physician before starting any new protocol. Now, explain exactly what you mean by needing the right raw materials for your aging joints.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Direct eye contact, analytical expression. No subtitles."
        },
        {
            "id": "A5",
            "speaker": "He", 
            "text": "Think about it like framing a custom house. You absolutely cannot build a solid foundation with rotten wood. Your body is the exact same way.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Speaking bluntly with a builder persona, hands shaping a box. No subtitles."
        },
        {
            "id": "A6",
            "speaker": "He", 
            "text": "Bending over used to be a chore. Now, it feels completely easy again. The absolute secret for my structure has been the Wolverine stack protocol.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Looking excited, slight camera pan left. No subtitles."
        },
        {
            "id": "A7",
            "speaker": "He", 
            "text": "I am running C-J-C twelve ninety five without D-A-C, combined with Ibutamoren. It physically provides the scaffolding my body needs to repair itself properly today.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Intense, blunt delivery. No subtitles."
        },
        {
            "id": "A8",
            "speaker": "He", 
            "text": "At two hundred ten pounds, carrying that kind of mass around the job site takes a massive toll on your connective tissue and recovery times.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees right. Expressive hand gestures. No subtitles."
        },
        {
            "id": "A9",
            "speaker": "He", 
            "text": "This stack optimizes the natural growth pulses. It is not masking the pain at all, it is actually physically repairing the micro tears every night.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, authoritative builder persona. Camera slowly pushes in. No subtitles."
        },
        {
            "id": "A10",
            "speaker": "He", 
            "text": "So my mobility is totally back. I am moving fluidly, and honestly, feeling like I am twenty years old again when I wake up morning.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Cinematic shot. Looking very happy, relaxed body language. No subtitles."
        },
        {
            "id": "A11",
            "speaker": "She", 
            "text": "That structural repair is truly fascinating. The C-J-C and Ibutamoren combination clearly works for your specific biological scaffolding. But let us shift our gears completely.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. Slight zoom out. No subtitles."
        },
        {
            "id": "A12",
            "speaker": "She", 
            "text": "Structure is one thing, but what about the power grid? The biohacking space is currently blowing up over a brand new mitochondrial derived peptide compound.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. Camera pans slightly left. No subtitles."
        },
        {
            "id": "A13",
            "speaker": "She", 
            "text": "It is called MOTS-c. If the Wolverine stack is the scaffolding, MOTS-c is the electrical grid keeping the lights on inside your actual cells today.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Hand gestures emphasizing energy. Slow zoom in. No subtitles."
        },
        {
            "id": "A14",
            "speaker": "She", 
            "text": "There is actually a massive clinical trial happening right now, looking at how MOTS-c acts like literal exercise in a bottle for the human body.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on eyes and face. Highly engaged expression. No subtitles."
        },
        {
            "id": "A15",
            "speaker": "He", 
            "text": "Exercise in a bottle. That sounds like a complete cheat code. How exactly does a peptide target the mitochondria directly like that in the body?",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees left. Curious, blunt tone. No subtitles."
        },
        {
            "id": "A16",
            "speaker": "She", 
            "text": "It prevents cellular senescence. Basically, it stops your cells from acting old and tired, restoring mitochondrial respiration so you naturally produce far more metabolic energy.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Speaking with authority, slow dolly push-in. No subtitles."
        },
        {
            "id": "A17",
            "speaker": "He", 
            "text": "So while my personal stack is physically rebuilding the joints and muscles, MOTS-c would theoretically provide the pure cellular energy to fuel that massive rebuilding.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Excited builder persona, hands moving. No subtitles."
        },
        {
            "id": "A18",
            "speaker": "She", 
            "text": "Exactly right. It improves insulin sensitivity and directly combats aging related diseases. The published data on PubMed right now is honestly absolutely staggering to read.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, analytical expression. Camera holds steady. No subtitles."
        },
        {
            "id": "A19",
            "speaker": "He", 
            "text": "That is the ultimate metabolic remodeling. You handle the structure with the Wolverine stack, and you handle the entire engine with the MOTS-c peptide. Incredible.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Very happy, expressive hand gestures, slow zoom-out. No subtitles."
        },
        {
            "id": "A20",
            "speaker": "She", 
            "text": "We will keep monitoring the clinical trials closely on MOTS-c. For now, your case study proves that getting the right raw materials changes absolutely everything.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Cinematic shot, slow dolly push-in. Smiling slightly. No subtitles."
        },
        {
            "id": "A21",
            "speaker": "He",
            "text": "And when you are training, you are not just lifting weights. You are building the infrastructure. If the scaffolding is weak, the whole structure collapses.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees right. Blunt delivery, expressive hands. No subtitles."
        },
        {
            "id": "A22",
            "speaker": "She",
            "text": "Exactly. That is why clinical focus on peptides like C-J-C twelve ninety five is about supporting that cellular scaffold, not forcing unnatural growth pulses.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Camera slowly zooms in. Analytical expression. No subtitles."
        },
        {
            "id": "A23",
            "speaker": "He",
            "text": "Right. It is a titration schedule, a gradual building process. We are not looking for a quick fix here. It is about long term sustainability.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Builder persona, talking blunt. No subtitles."
        },
        {
            "id": "A24",
            "speaker": "She",
            "text": "And titration is key to avoiding receptor desensitization. If you run it too hard, too fast, your body simply stops responding properly over time.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Professional posture, looking slightly off-camera. Speaking clearly. No subtitles."
        },
        {
            "id": "A25",
            "speaker": "He",
            "text": "Like over stressing a beam on a job site. You exceed the load capacity, and something is going to snap. You have to titrate the stress.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Blunt delivery, hand making a snapping motion. No subtitles."
        },
        {
            "id": "A26",
            "speaker": "She",
            "text": "Correct. And when you look at the research on MOTS-c, it is doing the same thing for the metabolic side. It titrates the energy production.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Direct eye contact. No subtitles."
        },
        {
            "id": "A27",
            "speaker": "He",
            "text": "So we are optimizing the metabolic blueprint. Rebuilding the scaffolding with C-J-C and Ibutamoren, and optimizing the power grid with the MOTS-c peptide.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees left. Excited tone, hands moving. No subtitles."
        },
        {
            "id": "A28",
            "speaker": "She",
            "text": "Exactly. But remember, the clinical data on MOTS-c is still developing. We are looking at rodent models and very early human trials right now.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. Slow zoom out. No subtitles."
        },
        {
            "id": "A29",
            "speaker": "He",
            "text": "Which is why we frame this as a personal case study. What works for my two hundred ten pound frame might not work for someone else.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Blunt delivery, pointing to chest. No subtitles."
        },
        {
            "id": "A30",
            "speaker": "She",
            "text": "Precisely. Individual biochemistry is highly variable. What we are showing is the conceptual framework of structural repair combined with cellular energy production.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. Camera holds steady. No subtitles."
        },
        {
            "id": "A31",
            "speaker": "He",
            "text": "And that conceptual framework is what is missing in most standard anti aging protocols. People focus on one hormone without looking at mitochondria.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Blunt delivery. No subtitles."
        },
        {
            "id": "A32",
            "speaker": "She",
            "text": "Right. Without mitochondrial respiration, you cannot synthesize the proteins needed for tissue repair. The engine needs fuel to build the house properly.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Speaking clearly. No subtitles."
        },
        {
            "id": "A33",
            "speaker": "He",
            "text": "Beautifully put. You need the power on site before you start framing. Otherwise, you are just standing in the dark with a hammer.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Excited builder persona, laughing slightly. No subtitles."
        },
        {
            "id": "A34",
            "speaker": "She",
            "text": "And the research shows MOTS-c actually promotes mitochondrial biogenesis. It is literally building more power plants inside your actual cells today.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. Slow zoom in. No subtitles."
        },
        {
            "id": "A35",
            "speaker": "He",
            "text": "Building more power plants. That is how we fight cellular senescence. We keep the cellular power grid expanding instead of decaying slowly.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Blunt delivery. No subtitles."
        },
        {
            "id": "A36",
            "speaker": "She",
            "text": "Exactly. And a robust power grid means better insulin sensitivity, less inflammation, and faster recovery from intense physical training in the gym.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Camera slowly pushes in. No subtitles."
        },
        {
            "id": "A37",
            "speaker": "He",
            "text": "Which directly correlates to how I am feeling. Moving easily, bending over, no morning stiffness. It is all connected to that cellular energy.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees right. Happy expression. No subtitles."
        },
        {
            "id": "A38",
            "speaker": "She",
            "text": "It is. But safety is paramount. Any case study needs to emphasize clean sources and regular blood work to monitor systemic health closely.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. No subtitles."
        },
        {
            "id": "A39",
            "speaker": "He",
            "text": "Absolutely. You don't build a custom house without inspecting the foundation regularly. Blood work is your essential structural inspection.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees left. Blunt builder persona. No subtitles."
        },
        {
            "id": "A40",
            "speaker": "She",
            "text": "And that is the core takeaway. Remodeling the aging machine requires a highly systematic, data driven approach, not random guesswork.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. No subtitles."
        },
        {
            "id": "A41",
            "speaker": "He",
            "text": "Systematic approach. We check the blueprints, we measure the loads, and we adjust the protocols based on real feedback.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, natural hand gestures. No subtitles."
        },
        {
            "id": "A42",
            "speaker": "She",
            "text": "Exactly. And we share this data for educational study, hoping it inspires men to look deeper into their own metabolic health.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Speaking clearly. No subtitles."
        },
        {
            "id": "A43",
            "speaker": "He",
            "text": "That is the goal. Rebuilding the machine while it is still running. It is hard work, but the results speak for themselves.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Smiling, hands moving. No subtitles."
        },
        {
            "id": "A44",
            "speaker": "She",
            "text": "It is a continuous process. And we will keep tracking the science as new clinical trials on mitochondrial peptides emerge.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. No subtitles."
        },
        {
            "id": "A45",
            "speaker": "He",
            "text": "Speaking of keeping the engine running perfectly, you have to lock in your mental focus when you actually get into the gym to do the work.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Excited persona, hands gesturing widely. No subtitles."
        },
        {
            "id": "A46",
            "speaker": "He",
            "text": "I have been bumping our new Keystone Recomposition deep house mix on Spotify. It is the perfect training soundscape to completely soundtrack your entire workout.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Happy expression. No subtitles."
        },
        {
            "id": "A47",
            "speaker": "He",
            "text": "The link is down in the description below. Hit subscribe right now if you are following the journey, and drop a comment on our next topic.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees left. Blunt delivery. No subtitles."
        },
        {
            "id": "A48",
            "speaker": "She",
            "text": "Stay consistent, stay curious, and always verify the science behind the protocol. Thanks for tuning in to another episode of the Recomposition case studies right now.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. Slow zoom out. No subtitles."
        },
        {
            "id": "A49",
            "speaker": "He",
            "text": "Build the foundation correctly, and the rest of the house will absolutely stand the test of time. Keep putting in the work every single day guys.",
            "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Smiling, builder persona, hands moving. No subtitles."
        },
        {
            "id": "A50",
            "speaker": "She",
            "text": "We will see you in the next breakdown where we dive even deeper into cellular energy and metabolic remodeling. Check the links below for the soundscapes.",
            "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Friendly, engaging expression. No subtitles."
        }
    ];

    const delay = ms => new Promise(res => setTimeout(res, ms));

    const waitForSelector = async (selector, timeout = 10000) => {
        const start = Date.now();
        while (Date.now() - start < timeout) {
            const el = document.querySelector(selector);
            if (el && el.offsetHeight > 0) return el;
            await delay(100);
        }
        throw new Error(`Timeout waiting for selector: ${selector}`);
    };

    window.flowAutomationStatus = {
        currentClip: null,
        status: "starting",
        submitted: [],
        errors: [],
        stop: false
    };

    console.log("Starting Slate-powered Google Flow automation loop (starting from A2)...");

    (async () => {
        // Start from index 1 which corresponds to Clip A2
        for (let i = 1; i < clips.length; i++) {
            if (window.flowAutomationStatus.stop) {
                console.log("Automation stopped by user request.");
                window.flowAutomationStatus.status = "stopped";
                return;
            }

            const clip = clips[i];
            window.flowAutomationStatus.currentClip = clip.id;
            window.flowAutomationStatus.status = `processing ${clip.id}`;
            console.log(`Processing Clip ${clip.id} (${clip.speaker})`);

            try {
                // 1. Get prompt textbox element
                const box = document.querySelector('[role="textbox"]');
                if (!box) throw new Error("textbox not found");
                box.focus();
                await delay(300);

                // Find the React Slate editor instance on the textbox element
                const fiberKey = Object.keys(box).find(k => k.startsWith('__reactFiber'));
                const fiber = box[fiberKey];
                let curr = fiber;
                let editor = null;
                while (curr) {
                    if (curr.memoizedProps && curr.memoizedProps.editor) {
                        editor = curr.memoizedProps.editor;
                        break;
                    }
                    curr = curr.return;
                }
                if (!editor) throw new Error("Slate editor instance not found");

                // 2. Clear character tags cleanly by programmatically clicking cancel buttons
                const cancelBtns = Array.from(document.querySelectorAll('button')).filter(b => {
                    const text = b.textContent;
                    return text.includes('cancelaccount_circle') || text.includes('cancelaccessibility_new');
                });
                for (const btn of cancelBtns) {
                    btn.click();
                    await delay(300);
                }

                // 3. Wiping existing text cleanly using Slate Editor API
                while (editor.children.length > 0) {
                    editor.apply({ type: 'remove_node', path: [0], node: editor.children[0] });
                }
                editor.apply({ type: 'insert_node', path: [0], node: { type: 'paragraph', children: [{ text: '' }] } });
                await delay(300);

                // 4. Type prompt using Slate Editor API
                const pronoun = clip.speaker.toLowerCase() === "he" ? "He" : "She";
                const fullPrompt = `${pronoun} says: ${clip.text}. ${clip.direction}`;
                editor.insertText(fullPrompt);
                box.dispatchEvent(new Event('input', { bubbles: true })); // notify React editor wrappers
                await delay(500);

                // 5. Open asset picker dialog
                const addBtn = document.querySelector('[aria-haspopup="dialog"]') || document.querySelector('[class*="add_2"]');
                if (!addBtn) throw new Error("add button not found");
                addBtn.click();
                
                // Wait for dialog element to appear in DOM
                const dialog = await waitForSelector('[role="dialog"]', 10000);

                // 6. Select correct tab and click image card inside picker dialog
                const tabs = Array.from(dialog.querySelectorAll('[role="tab"]'));
                if (clip.speaker.toLowerCase() === "he") {
                    const avatarTab = tabs.find(t => t.textContent.includes('Avatar'));
                    if (!avatarTab) throw new Error("Avatar tab not found");
                    avatarTab.click();
                    
                    // Wait for alt='me' image to render
                    const img = await waitForSelector('img[alt="me"]', 10000);
                    const card = img.closest('button') || img.closest('[class*="sc-"]') || img.parentElement;
                    card.click();
                    await delay(500);
                } else {
                    const charTab = tabs.find(t => t.textContent.includes('Characters'));
                    if (!charTab) throw new Error("Characters tab not found");
                    charTab.click();
                    
                    // Wait for alt='Victoria' image to render
                    const img = await waitForSelector('img[alt="Victoria"]', 10000);
                    const card = img.closest('a');
                    if (card) {
                        const preventNav = (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                        };
                        card.addEventListener('click', preventNav, { capture: true });
                        card.click();
                        await delay(100);
                        card.removeEventListener('click', preventNav, { capture: true });
                    } else {
                        img.click();
                    }
                    await delay(500);
                }

                // 7. Click Add to Prompt
                const addPromptBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.textContent.includes('Add to Prompt'));
                if (!addPromptBtn) throw new Error("Add to Prompt button not found");
                addPromptBtn.click();
                
                // Wait for the dialog to disappear
                await delay(1000);

                // 8. Submit Create (arrow_forward)
                const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('arrow_forward'));
                if (!submitBtn) throw new Error("submitBtn not found");
                submitBtn.click();
                
                console.log(`Submitted Clip ${clip.id}`);
                window.flowAutomationStatus.submitted.push(clip.id);
                await delay(1500);

            } catch (err) {
                console.error(`Error processing ${clip.id}: ${err.message}`);
                window.flowAutomationStatus.status = "error";
                window.flowAutomationStatus.errors.push({ clip: clip.id, error: err.message });
                return;
            }

            // Batches of 4 (A2 is index 1, A3 is 2, A4 is 3, A5 is 4... so index i % 4 logic)
            // Since we start from i = 1 (A2), index 1,2,3,4 (which is A2, A3, A4, A5) is the first batch of 4.
            // Let's pace after A5, A9, A13, etc. (i % 4 === 0)
            if (i % 4 === 0 && i < clips.length - 1) {
                console.log("Batch complete. Waiting 20 seconds...");
                window.flowAutomationStatus.status = "waiting_20s";
                await delay(20000);
            }
        }

        window.flowAutomationStatus.status = "completed";
        console.log("All clips submitted successfully!");
    })();

    return "Started background automation";
})();
