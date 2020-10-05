import React from 'react';
import ReactPlayer from "react-player";

const AdditionalResources = () =>(
    <div>
        
        <div class="jumbotron">
        <h2>Additional Resources About American Sign Language</h2>
        <div>&nbsp;</div>
           <ul>
                <li><a href="https://www.nidcd.nih.gov/health/american-sign-language">National Institute on Deafness and Other Communication Disorders (NIDCD)</a></li>
                <p>The National Institute on Deafness and Other Communication Disorders (NIDCD), part of the National Institutes of Health (NIH), conducts and supports research in the normal and disordered processes of hearing, balance, taste, smell, voice, speech, and language.</p>
                <li><a href="https://www.nad.org/resources/american-sign-language/">National Association of the Deaf</a></li>
                <p>The NAD values deaf and hard of hearing Americans with diverse perspectives, experiences, and abilities. We embrace diversity and inclusiveness as core values in achieving our mission. It is the philosophy of the NAD that diversity encompasses a wide range of human abilities and perspectives. The NAD is committed to building and maintaining an inclusive environment where differences of opinions, beliefs, and values are sought, respected, and valued.</p>
                <li><a href="http://www.signedlanguage.co.uk/HowToConveyEmotion.html">How to convey tone</a></li>
                <p>Body language is key when using sign language - and not just so the signs can be seen clearly, although this is important. But thankfully body language usually comes pretty naturally and conveys emotions without us needing to think about it. The only difference with sign language is that if you really want to get across a particular emotion, you may need to exaggerate the body language, so even more slouched if you are reluctant about something or bouncing around if you are happy. </p>
                <ReactPlayer url="https://www.youtube.com/watch?time_continue=1233&v=VX18-4m-EN0&feature=emb_title"/>
                <li><a href="https://www.signingsavvy.com/article/46/The+Importance+of+Facial+Expressions">Facial Expressions to show Emotion</a></li>
                <p>Facial expression plays a very important part in the meaning of a sign. The same exact hand-shape and movement can totally change meaning because of the facial expression that is used to accompany it.</p>
                <ReactPlayer url="https://www.youtube.com/watch?v=c2W6TVd_xh4"/>
            </ul>
        </div>
    </div>
)

export default AdditionalResources;