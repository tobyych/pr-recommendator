import spacy
import pytextrank

def get_name_entities(text):
  spacy_nlp = spacy.load('en_core_web_sm')
  tr = pytextrank.TextRank()
  spacy_nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
  doc = spacy_nlp(text)
  interested_entities = []
  for p in doc.ents:
    if p.label_ in ['PERSON', 'ORG']:
      interested_entities.append(p.text.lower())
  for p in doc._.phrases:
    if p.text in interested_entities:
     yield (p.text, p.rank)
  
  


if __name__ == '__main__':
  text = '''ByteDance is not backing down from its ambitions to become a global technology powerhouse, even as TikTok loses its largest market (India) and faces insurmountable challenges in the U.S. But some in China are blasting the Beijing-based company as too accommodating and yielding to U.S. demands.

ByteDance said it will “remain committed to our vision to become a globalized company” despite the flurry of challenges thrown at it, it said in a statement posted late Sunday.

Following months of efforts to sway U.S. regulators and the public, TikTok reluctantly arrived at two concessions: “We faced the real possibility of a forced sale of TikTok’s US business by CFIUS or an executive order banning on the TikTok app in the US,” ByteDance founder and CEO Zhang Yiming wrote to employees in a letter on Monday.

The TikTok saga is evolving on an hourly basis. As of writing, Microsoft has confirmed it’s in talks with U.S. officials to pursue a TikTok purchase. Trump previously said he would not support the purchase of the Chinese-owned app by an American company.

On the China end, Zhang told his staff that the company has “initiated preliminary discussions with a tech company to help clear the way for us to continue offering the TikTok app in the US.” The message corroborates reassurance from the app’s U.S. general manager Vanessa Pappas that TikTok is “not planning on going anywhere.”

Zhang is unabashed about his frustration in the letter: “We disagree with CFIUS’s conclusion because we have always been committed to user safety, platform neutrality, and transparency. However, we understand their decision in the current macro environment.”

Angry netizens

But ByteDance’s responses clearly have not won favor with some people in China. On Weibo, a popular microblogging platform in China, hundreds of anonymous users joined in under a post about Zhang’s letter, cursing him as a traitor of China, an American apologist and a coward, among many other labels.

“Zhang Yiming used to praise the US for allowing debate, unlike in China, where opinions are one-sided. Now he got a slap in the face, why doesn’t he go argue with the US?” chastised one of the most popular comments with more than 3,600 likes.

The commentator appears to be referring to some of Zhang’s Weibo posts from the early 2010s, which can be seen by some as liberal-leaning, putting the entrepreneur in the rank of “public intellectuals.” The term has in recent years been thought of as derogatory, as internet patriots see the group as ignorant and worshippers of Western values.

“The general view among Chinese social media users is that this is a tit-for-tat measure as part of the ongoing U.S.-China trade war. They also believe that these steps are being taken due to TikTok’s success and because it has now become a threat to U.S. platforms such as Facebook and Twitter,” said Rich Bishop, CEO of AppInChina, which helps international apps and games publish in China.

Zhang’s Weibo account is currently suspended, presumably to prevent armies of angry patriots from flooding his posts.

It’s hard to gauge how representative the online sentiment is of the Chinese public, or whether the discourse is orchestrated by government-paid commentators. Compared to the internet fury, though, Beijing appeared relatively resigned, with a Foreign Ministry spokesperson merely denying U.S. allegations against TikTok as fabricated “out of nothing” during a regular presser. (There’s no concrete evidence publicly presented by the U.S. government yet to support its claims that TikTok is a national security threat.)

After all, the Chinese government can’t do much to retaliate, given there are scant examples of American internet giants with a considerable business in China. There’s also little impetus for Beijing to stand up for ByteDance. Unlike Huawei, which provides the backbone of telecoms networks in China and many other countries, ByteDance is far from being seen as a “national champion.” The state-of-the-art content algorithms it claims to have, after all, are used to hook people to the screens.

If anything, the Party is probably warier of what people consume on Bytedance apps rather than viewing them as a strategic partner in China’s race to be a global tech leader.

Sympathy from peers

Startups and investors in China are more sympathetic toward ByteDance. Many agree that if the Microsoft deal goes through, it could be the least bad outcome for TikTok.

“They are stuck between a rock and a hard place,” said William Bao Bean, general partner at Chinaccelerator, a cross-border accelerator backed by SOSV. “We are in a fast-changing regulatory environment. I think the consumers would probably want to continue using the service, and this is one potential way to make that happen. Obviously, I don’t think it’s what ByteDance really wants.”

AppInChina’s Bishop reminded us of Microsoft’s non-confrontational attitude toward Beijing. “I think it’s a good outcome for all sides. Microsoft of course benefits hugely from getting into social media. ByteDance gets a good payout, and Bytedance and the Chinese government are relatively friendly towards Microsoft.”

The tech community is well aware that TikTok is a rarity. Although the backlash will have a chilling effect on Chinese companies expanding to the U.S., and potentially other Western markets, there simply aren’t many internet companies going from China to the West in the first place.

“Most solutions that are built for China don’t solve problems that people have in the West,” observed Bao Bean.

Chinese games probably have the best shot in conquering the West, as WeChat parent Tencent, through aggressive acquisitions and numerous smash-hits, has demonstrated. Smaller developers resort to the strategy of “laying low” about their Chinese origin.

“We simply don’t take media interviews,” said the CEO of a U.S.-listed Chinese internet firm on condition of anonymity.

“It’s not about the chilling effect. The problem is there won’t be opportunities in the U.S., Canada, Australia or India anymore. The chance of succeeding in Europe is also becoming smaller, and the risks are increasing a lot,” a former executive overseeing an American giant’s Chinese business lamented, asking not to be named.

“From now on, Chinese companies going global can only look to Southeast Asia, Africa and South America.”
'''
  get_name_entities(text)