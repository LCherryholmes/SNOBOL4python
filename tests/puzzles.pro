%-------------------------------------------------------------------------------
% 3
% Dorothy, Jean, Virginia, Bill, Jim, and Tom are six young persons who have
% been close friends from their childhood.They went through high school and
% college together, and when they finally paired off and became engaged nothing
% would do but a triple announcement party. Naturally they wanted to break the
% news to their friends in an unusual fashion, and after some thought they
% decided upon this scheme.  At just the right moment during the party everyone
% was given a card bearing the cryptic information:
%     Who now are six will soon be three,
%     And gaily we confess it,
%     But how we've chosen you may know
%     No sooner than you guess it.
% Tom, who is older than Jim, is Dorothy's brother.  Virginia is the oldest
% girl.  The total age of each couple-to-be is the same although no two of us
% are the same age.  Jim and Jean are together as old as Bill and Dorothy. What
% three engagements were announced at the party?
man(bill).
man(jim).
man(tom).
woman(dorothy).
woman(jean).
woman(virginia).
isOlder(tom, jim).
isOlder(virginia, dorothy).
isOlder(virginia, jean).
isBrother(tom, dorothy).
%-------------------------------------------------------------------------------
% 4
% Mr. Carter, Mr. Flynn, Mr. Milne, and Mr. Savage serve the little town of
% Milford as architect, banker, druggist, and grocer, though not necessarily
% respectively.  Each man's income is a whole number of dollars.  The druggist
% earns exactly twice as much as the grocer, the architect earns exactly twice
% as much as the druggist, and the banker earns exactly twice as much as the
% architect.  Although Mr. Carter is older than anyone who makes more money
% than Mr. Flynn, Mr. Flynn does not make twice as much as Mr. Carter.  Mr.
% Savage earns exactly $3776 more than Mr. Milne.
% What is each man's occupation?
:- initialization(main).
person(mr_carter).
person(mr_flynn).
person(mr_milne).
person(mr_savage).
main :-
   person(Architect),
   person(Banker),
   person(Druggist),
   person(Grocer),
   differ(Architect, Banker, Druggist, Grocer),
   display(Architect, Banker, Druggist, Grocer),
   fail.
%-------------------------------------------------------------------------------
% 7
% Brown, Clark, Jones and Smith are four substantial citizens who serve their
% community as architect, banker, doctor, and lawyer, though not necessarily
% respectively.
% Brown, who is more conservative than Jones butmore liberal than Smith, is a better golfer than the men
% who are younger than he is and has a larger income than the men who are older than Clark.
% The banker, who earns more than the architect, is neither the youngest nor the oldest.
% The doctor, who is a poorer golfer than the lawyer, is less conservative than the architect.
% As might be expected, the oldest man is the most conservative and has the largest income, and the youngest man is the best golfer.
% What is each man's profession?
% -----------------------------------------------------------------------------------------------------------------------
% 8
% In a certain department store the position of buyer, cashier,clerk, floorwalker, and manager are held, though not necessarily respectively, by Miss Ames, Miss Brown, Mr. Conroy,Mr. Davis, and Mr. Evans.
% The cashier and the manager were roommates incollege.
% The buyer is a bachelor.
% Evans and Miss Ames have had only business contacts with each other.
% Mrs. Conroy was greatly disappointed when her husband told her that the manager had refused to give hima raise.
% Davis is going to be the best man when the clerk andthe cashier are married.
% What position does each person hold?#-----------------------------------------------------------------------------------------------------------------------
% -----------------------------------------------------------------------------------------------------------------------
% 9
% The positions of buyer, cashier, clerk, floorwalker, and manager in the Empire Department Store are held by Messrs.Allen, Bennett, Clark, Davis, and Ewing.
% The cashier and the floorwalker eat lunch from 11:30to 12:30, the others eat from 12:30 to 1:30.
% Mrs. Allen and Mrs. Clark are sisters.
% Allen and Bennett always bring their lunch and playcribbage during their lunch hour.
% Davis and Ewing have nothing to do with each other
% since the day Davis, returning from lunch earlier thanusual, found Ewing already gone and reported him tothe manager.
% The cashier and the clerk share bachelor quarters.
% What position does each man fill?
% -----------------------------------------------------------------------------------------------------------------------
% 10
% Jane, Janice, Jack, Jasper, and Jim are the names of fivehigh school chums. Their last names in one order or anotherare Carter, Carver, Clark, Clayton, and Cramer.
% Jasper's mother is dead.
% In deference to a certain very wealthy aunt, Mr. andMrs. Clayton agreed when they were first married thatif they ever had a daughter they would name her Janice.Jane's father and mother have never met Jack'sparents.
% The Cramer and Carter children have been teammates on several of the school's athletic teams.
% When he heard that Carver was going to be out oftown on the night of the school's Father and Son banquet, Cramer called Mrs. Carver and offered to "adopt"her son for the evening, but Jack's father had alreadyasked him to go.
% The Clarks and Carters, who are very good friends,were delighted when their children began dating eachother.
% W hat is the full name of each youngster?#-----------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
% 11
% The Smith family, which consists of Mr. and Mrs. Smith,their son, Mr. Smith's sister, and Mrs. Smith's father, has foryears dominated the community life of Plainsville. At thepresent time the five members of the family hold among themselves the positions of grocer, lawyer, postmaster, preacher,and teacher in the little town.
% The lawyer and the teacher are not blood relatives.The grocer is younger than her sister-in-law but older
% than the teacher.
% The preacher, who won his letter playing football incollege, is older than the postmaster.
% What position does each member of the family hold?#-----------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
% 12
% In the Stillwater High School the economics, English,French, history, Latin, and mathematics classes are taught,though not necessarily respectively, by Mrs. Arthur, Miss Bascomb, Mrs. Conroy, Mr. Duval, Mr. Eggleston, and Mr. Furness.The mathematics teacher and the Latin teacher were
% roommates in college.
% Eggleston is older than Furness but has not taughtas long as the economics teacher.
% As students, Mrs. Arthur and Miss Bascomb attendedone high school while the others attended a differenthigh school.
% Furness is the French teacher's father.
% The English teacher is the oldest of the six both inage and in years of service. In fact he had the mathematics teacher and the history teacher in class whenthey were students in the Stillwater High School.
% Mrs. Arthur is older than the Latin teacher.
% What subject does each person teach?
%-------------------------------------------------------------------------------
% 13
% A recent murder case centered around the six men, Clayton,Forbes, Graham, Holgate, McFee, and Warren. In one order
% or another these men were the victim, the murderer, the witness, the policeman, the judge, and the hangman. The facts
% of the case were simple. The victim had died instantly from
% the effect of a gunshot wound inflicted at close range. The
% witness did not see the crime committed, but swore to hearing an altercation followed by a shot. After a lengthy trial themurderer was convicted, sentenced to death, and hanged.
% McFee knew both the victim and the murderer.
% In court the judge asked Clayton to give his account
% of the shooting.
% Warren was the last of the six to see Forbes alive.
% The policeman testified that he picked up Grahamnear the place where the body was found.
% Holgate and Warren never met.
% What role did each man play in this unfortunatemelodraта?#-----------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
% 14
% One fine spring afternoon Bill, Ed, and Tom with theirwives, whose names in one order or another are Grace, Helen,and Mary, went out and played eighteen holes of golf together.Mary, Helen, Grace, and Ed shot 106, 102, 100, and94 respectively.
% Bill and Tom shot a 98 and a 96, but for some timethey couldn't tell who had made which since they hadn'tput their names on their scorecards.
% When the fellows finally identified their cards itturned out that two of the couples had the same totalscore.
% Ed's wife beat Bill's wife.
% What is the name of each man's wife, and what scores
% did Bill and Tom make?#-----------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
% 15
% Vernon, Wilson, and Yates are three professional men, one
% an architect, one a doctor, and one a lawyer, who occupy officeson different floors of the same building. Their secretaries are
% named, though not necessarily respectively, Miss Ainsley,Miss Barnette, and Miss Coulter.
% The lawyer has his office on the ground floor.
% Instead of marrying her boss the way secretaries doin stories, Miss Barnette became engaged to Yates andgoes out to lunch with him every day.
% At noon Miss Ainsley goes upstairs to eat lunch withWilson's secretary.
% Vernon had to send his secretary down to borrowsome stamps from the architect's office the other day.What is each man's profession, and what is the name
% of each man's secretary?
%-------------------------------------------------------------------------------
% 16
% The crew of a certain train consists of a brakeman, a conductor, an engineer, and a fireman, named in one order or another Art, John, Pete, and Tom.
% John is older than Art.
% The brakeman has no relatives on the crew.
% The engineer and the fireman are brothers.
% John is Pete's nephew.
% The fireman is not the conductor's uncle, and the conductor is not the engineer's uncle.
% What position does each man hold, and how are themen related?
%-------------------------------------------------------------------------------
% 17
% Ed, Frank, George, and Harry took their wives to theCountry Club dance one Saturday evening not long agc. Atone time as a result of exchanging dances Betty was dancingwith Ed, Alice was dancing with Carol's husband, Dorothywas dancing with Alice's husband, Frank was dancing withGeorge's wife, and George was dancing with Ed's wife.
% What is the name of each man's wife, and with whomwas each man dancing?
%-------------------------------------------------------------------------------
% 18
% During the summer in Luncyville the shoe store is closed every Monday, the hardware store is closed every Tuesday, the
% grocery store is closed every Thursday, and the bank is open
% only on Monday, Wednesday, and Friday. Everything of course
% is closed on Sunday. One afternoon Mrs. Abbott, Mrs. Briggs,Mrs. Culver, and Mrs. Denny went shopping together, eachwith a different place to go. On their way they dropped thefollowing remarks:
% Mrs. Abbott: Mrs. Denny and I wanted to go earlier inthe week but there wasn't a day when we
% could both take care of our errands.
% Mrs. Briggs I didn't want to come today but tomorrow
% I couldn't do what I have to do.
% Mrs. Culver: I could have gone yesterday or the daybefore just as well as today.
% Mrs. Denny: Either yesterday or tomorrow would havesuited me.
% Which place did each woman need to visit in town?#-----------------------------------------------------------------------------------------------------------------------
%-------------------------------------------------------------------------------
% 19
% Allen, Brady, McCoy, and Smith are the names of four men
% who have offices on different floors of the same eighteen storybuilding. One of the men is an accountant, one an architect,one a dentist, and one a lawyer.
% Allen's office is on a higher floor than McCoy's, although it is lower than Smith's.
% Brady's office is below the dentist's.
% Smith's office is five times as high as the lawyer'soffice.
% If the architect were to move up two floors he wouldbe halfway between the dentist and the accountant, andif he were to move his office halfway down he wouldthen be midway between the floors where the offices ofthe dentist and the lawyer are located.
% In this particular building the groundfloor is devoted toshops of various kinds and contains no office space. Hence asfar as the offices in the building are concerned the first flooris the one immediately above the groundfloor.
% What is each man's profession
%-------------------------------------------------------------------------------
% 20
% Four men, one a famous historian, another a poet, the thirdnovelist, and the fourth a playwright, named, though not
% necessarily respectively, Adams, Brown, Clark, and Davis, once
% found themselves seated together in a pullman car. Happeningto look up simultaneously from their reading, they discoveredthat each was occupied with a book by one of the others.Adams and Brown had just a few minutes before finished the
% books they had brought and had exchanged with each other.The poet was reading a play. The novelist, who was a very
% young man with only one book to his credit, boasted that he
% had never so much as opened a book of history in his life.Brown had brought one of Davis' books, and none of the othershad brought one of his own books either
% What was each man reading, and what was each man's
% literary field?
#-----------------------------------------------------------------------------------------------------------------------
