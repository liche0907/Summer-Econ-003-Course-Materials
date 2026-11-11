const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,LevelFormat,AlignmentType,
       Table,TableRow,TableCell,WidthType,ShadingType}=require('docx');
const NAVY='1A365D', INK='222222', MUT='666666', ACC='B45F06', F='\u7b49\u7ebf';
const t=(x,o={})=>new TextRun({text:x,font:F,...o});
const p=o=>new Paragraph(o);
const H=x=>p({heading:HeadingLevel.HEADING_1,spacing:{before:340,after:120},
  children:[t(x,{bold:true,size:32,color:NAVY})]});
const S=x=>p({spacing:{before:180,after:70},children:[t(x,{bold:true,size:23,color:NAVY})]});
const B=x=>p({spacing:{after:80},children:[t(x,{size:22,color:INK})]});
const D=(term,def)=>p({spacing:{after:80},children:[t(term+' — ',{bold:true,size:22,color:INK}),t(def,{size:22,color:INK})]});
const L=x=>p({numbering:{reference:'b',level:0},spacing:{after:56},children:[t(x,{size:22,color:INK})]});
const Lb=(term,def)=>p({numbering:{reference:'b',level:0},spacing:{after:56},
  children:[t(term+' — ',{bold:true,size:22,color:INK}),t(def,{size:22,color:INK})]});
const FM=x=>p({spacing:{after:60},indent:{left:280},shading:{type:ShadingType.CLEAR,fill:'F2F5FA'},
  children:[t('  '+x+'  ',{size:22,bold:true,color:NAVY})]});
const GT=(lines)=>[p({spacing:{before:140,after:60},children:[t('Graphs and tables you must be able to read',{bold:true,size:21,color:ACC})]})]
  .concat(lines.map(x=>p({numbering:{reference:'b',level:0},spacing:{after:50},children:[t(x,{size:21,color:INK})]})));

const k=[];
k.push(p({spacing:{after:40},children:[t('ECON 003',{bold:true,size:56,color:NAVY})]}));
k.push(p({spacing:{after:120},children:[t('Midterm Exam Study Guide',{bold:true,size:40,color:NAVY})]}));
k.push(p({spacing:{after:40},children:[t('Saturday, August 15, 2026  |  10:00 AM – 12:00 PM (Pacific)',{size:23,color:INK})]}));
k.push(p({spacing:{after:40},children:[t('50 multiple-choice questions, drawn at random  |  Chapters 1, 3, 4, 5, 6',{size:23,color:INK})]}));
k.push(p({spacing:{after:40},children:[t('Online, open note  |  30% of the course grade',{size:23,color:INK})]}));
k.push(p({spacing:{after:240},border:{bottom:{style:BorderStyle.SINGLE,size:10,color:NAVY}},children:[t('')]}));

k.push(S('How the 50 questions are split'));
k.push(new Table({columnWidths:[2200,1500,1500,3600],rows:[
  ['Chapter','Questions','Of which harder','Where the weight sits'],
  ['1 — Principles and Practice','6','2','§1.1 scope, §1.3 optimization'],
  ['3 — Optimization','8','2','§3.2 levels, §3.3 the margin'],
  ['4 — Demand, Supply, Equilibrium','12','4','§4.2 buyers, §4.4 equilibrium'],
  ['5 — Consumers and Incentives','12','4','§5.2 the buyer’s problem, §5.5 elasticity'],
  ['6 — Sellers and Incentives','12','4','§6.2 the seller’s problem'],
].map((r,i)=>new TableRow({children:r.map((c,j)=>new TableCell({
  width:{size:[2200,1500,1500,3600][j],type:WidthType.DXA},
  margins:{top:60,bottom:60,left:110,right:110},
  shading:i===0?{type:ShadingType.CLEAR,fill:'E8EDF5'}:undefined,
  children:[p({children:[t(c,{size:20,bold:i===0,color:INK})]})]}))}))}));

k.push(S('Not on this exam'));
k.push(B('Everything below appeared on the winter final and is out of scope here. Do not spend time on it.'));
[ 'Chapter 2 in its entirety — production possibilities frontier, comparative and absolute advantage, gains from trade.',
  'Taxes, tax incidence, tax revenue and deadweight loss.',
  'Externalities, social cost and benefit, the Coase theorem, public goods and common resources.',
  'Monopoly, natural monopoly, price discrimination, and any comparison of market structures.',
  'Appendix 5.A (indifference curves) and Appendix 6.A (firms with different cost structures).',
  'The Evidence-Based Economics feature at the end of each chapter.'].forEach(x=>k.push(L(x)));

k.push(H('Key Notation'));
[['P','price'],['Q','quantity'],['QD','quantity demanded'],['QS','quantity supplied'],
 ['D, S','demand curve, supply curve'],['WTP','willingness to pay (a buyer’s reservation price)'],
 ['WTA','willingness to accept (a seller’s reservation price)'],['MB','marginal benefit'],
 ['MC','marginal cost'],['MR','marginal revenue'],['MP','marginal product'],
 ['TB, TC','total benefit, total cost'],['TR','total revenue'],['FC, VC','fixed cost, variable cost'],
 ['AFC, AVC, ATC','average fixed, average variable, average total cost'],
 ['CS, PS','consumer surplus, producer surplus'],
 ['E','elasticity'],['SR, LR','short run, long run'],['Δ','change in']
].forEach(([a,b])=>k.push(Lb(a,b)));

/* ---------------- CHAPTER 1 ---------------- */
k.push(H('Chapter 1 — The Principles and Practice of Economics'));
k.push(S('§1.1  The Scope of Economics'));
k.push(D('Economics','the study of how agents choose to allocate scarce resources and how those choices affect society.'));
k.push(D('Scarce resources','resources with a limited supply, so that using them for one purpose means giving up another.'));
k.push(D('Economic agent','an individual or a group that makes choices — a person, a household, a firm, a government.'));
k.push(D('Microeconomics','the study of how individuals, households and firms make choices, and how those choices interact in markets.'));
k.push(D('Macroeconomics','the study of the economy as a whole — growth, unemployment, inflation.'));
k.push(B('Be able to sort an example into micro or macro. Anything about one buyer, one firm or one market is micro; anything about aggregate output, the price level or national unemployment is macro.'));

k.push(S('§1.2  Three Principles of Economics'));
k.push(Lb('Optimization','choosing the best feasible option given the information and constraints you have.'));
k.push(Lb('Equilibrium','a situation in which nobody would benefit by changing their own behaviour, because everyone is already optimizing.'));
k.push(Lb('Empiricism','using data and evidence to test ideas about how the world works.'));
k.push(B('Given a described situation, you should be able to name which principle it illustrates — and note that one situation can illustrate more than one.'));

k.push(S('§1.3  The First Principle: Optimization'));
k.push(D('Trade-off','because resources are scarce, more of one thing means less of another.'));
k.push(D('Opportunity cost','the value of the best alternative you give up when you make a choice. It counts even when no money changes hands — forgone wages and forgone time are opportunity costs.'));
k.push(D('Budget constraint','the set of choices that exactly exhaust your available resources.'));
k.push(B('The most common error on this material is leaving out a cost that nobody billed you for. If a choice takes four hours and you could have earned $12 an hour, $48 is part of its cost.'));

k.push(S('§1.4  The Second Principle: Equilibrium'));
k.push(B('At a market equilibrium price, three things hold at once: the quantity buyers want equals the quantity sellers want to sell; sellers’ costs are covered by the price; and buyers value the good at least as much as the price. What is not true in equilibrium is that either side could still gain by changing its behaviour — if that were possible, you would not be at equilibrium.'));
k.push(D('Free riding','enjoying a benefit you cannot be shut out of, without contributing toward its cost.'));
k.push(B('Free riding sits in Chapter 1 because it is a consequence of optimization, not a separate topic. If the benefit reaches you whether or not you contribute, then contributing costs you something and changes what you receive hardly at all \u2014 so for each person individually, not contributing is the best feasible option. Everyone would be better off if everyone contributed, and yet nobody individually wants to. This is the first place in the course where individual optimization and the best group outcome come apart.'));
k.push(B('Exam phrasing: the textbook states this as \u201cthe private benefit of free riding exceeds its private cost.\u201d That is the same idea compressed \u2014 the benefit you keep by not paying is larger than anything you lose by not paying.'));

k.push(S('§1.5  The Third Principle: Empiricism'));
k.push(B('Economists test theories against data. Correlation between two variables is not by itself evidence that one causes the other.'));
k.push(D('Positive analysis','describes what is — a claim that can be checked against evidence.'));
k.push(D('Normative analysis','prescribes what ought to be — a claim that rests on a value judgement.'));
k.push(B('Optimization is used both ways: positively, to describe and predict the choices people actually make, and normatively, to advise them on how to choose better. An exam question asks exactly this, and the answer is BOTH, not one or the other.'));
k.push(...GT([
  'Nothing graphical is tested from Chapter 1 — the questions here are definitional and conceptual.']));

/* ---------------- CHAPTER 3 ---------------- */
k.push(H('Chapter 3 — Optimization'));
k.push(S('§3.1  Choosing the Best Feasible Option'));
k.push(D('Feasible option','an option you can actually afford and actually carry out, given your constraints.'));
k.push(D('Net benefit','benefit minus cost.'));
k.push(FM('Net benefit  =  total benefit  −  total cost'));
k.push(B('Optimization means picking the option with the highest net benefit among the feasible ones. An option that looks best overall but breaks the budget is not the answer — check feasibility first, then rank.'));

k.push(S('§3.2  Optimization in Levels'));
k.push(B('Compute the net benefit (or total cost) of each whole option and compare the levels directly. The chapter’s worked case is choosing an apartment: rent falls with distance from campus while commuting cost rises, so the optimum is the distance that minimizes rent plus commuting cost — not the cheapest rent.'));
k.push(B('Commuting cost is usually the value of the time, so it moves with your wage. If the value of your time rises, living close becomes relatively more attractive.'));
k.push(FM('Total cost of a location  =  rent  +  (hours of commuting × value per hour)'));

k.push(S('§3.3  Optimization in Differences — Marginal Analysis'));
k.push(D('Marginal benefit','the additional benefit from one more unit.'));
k.push(D('Marginal cost','the additional cost from one more unit.'));
k.push(B('Rule: keep expanding the activity as long as marginal benefit is at least as large as marginal cost. Stop at the last unit where MB ≥ MC.'));
k.push(FM('Optimum:  expand while  MB ≥ MC;  the optimum is where  MB = MC'));
k.push(B('Optimization in levels and optimization in differences always give the same answer. That is why you can find the peak of a net-benefit column either by scanning it or by applying the margin rule — a favourite exam point.'));
k.push(B('Optimization does not claim people always choose perfectly. It claims optimization is a good approximation of the choices people make — accurate enough to predict behaviour, without assuming anyone computes flawlessly.'));
k.push(D('Marginal versus average','marginal is the benefit or cost of one more unit; average is the benefit or cost per unit across all units. They are not interchangeable.'));
k.push(...GT([
  'A total-benefit or net-benefit column: compute marginal values by differencing consecutive rows.',
  'A marginal benefit and marginal cost table: find the last row where MB ≥ MC.',
  'A bar chart of marginal benefit against a flat marginal cost: read off where they cross.']));

/* ---------------- CHAPTER 4 ---------------- */
k.push(H('Chapter 4 — Demand, Supply, and Equilibrium'));
k.push(S('§4.1  Markets'));
k.push(D('Perfectly competitive market','a market in which the good is standardized, there are many buyers and many sellers, everyone takes the market price as given, information is full, and firms can enter and leave freely.'));
k.push(B('If any one seller is large enough to move the price, the market is not perfectly competitive.'));

k.push(S('§4.2  How Buyers Behave'));
k.push(D('Demand schedule','a table giving quantity demanded at each price. A demand curve plots it, and it slopes downward.'));
k.push(D('Law of demand','holding all else constant, a higher price means a lower quantity demanded.'));
k.push(D('Willingness to pay','the most a buyer would pay for a unit.'));
k.push(D('Diminishing marginal benefit','each additional unit consumed is worth less than the one before, which is why willingness to pay falls as quantity rises.'));
k.push(B('Market demand is the horizontal sum of individual demand curves: fix a price, add up the quantities each buyer wants at that price. Do not average them.'));
k.push(B('A change in the good’s own price is a movement along the demand curve. Everything else shifts it.'));
k.push(Lb('The five demand shifters','tastes and preferences; income and wealth; availability and price of related goods (substitutes and complements); number and scale of buyers; buyers’ beliefs about the future.'));
k.push(B('Substitutes: the price of one rises, demand for the other rises. Complements: the price of one rises, demand for the other falls. Normal good: income rises, demand rises. Inferior good: income rises, demand falls.'));

k.push(S('§4.3  How Sellers Behave'));
k.push(D('Law of supply','holding all else constant, a higher price means a higher quantity supplied.'));
k.push(D('Willingness to accept','the least a seller would accept for a unit. It equals the seller’s marginal cost of that unit, which is why the supply curve is a marginal cost curve read sideways.'));
k.push(B('Market supply is the horizontal sum of individual supply curves.'));
k.push(Lb('The four supply shifters','prices of inputs used in production; technology; number and scale of sellers; sellers’ beliefs about the future.'));
k.push(B('The price of the good itself is not a shifter — it moves you along the supply curve. Expecting a higher price later makes a seller hold back supply now, shifting the curve left.'));

k.push(S('§4.4  Supply and Demand in Equilibrium'));
k.push(D('Competitive equilibrium','the price at which quantity supplied equals quantity demanded.'));
k.push(D('Excess demand (shortage)','quantity demanded exceeds quantity supplied; happens when price is below equilibrium.'));
k.push(D('Excess supply (surplus)','quantity supplied exceeds quantity demanded; happens when price is above equilibrium.'));
k.push(B('Read a shortage or surplus off a graph as the horizontal gap between the two curves at the stated price — not as a distance from the old equilibrium.'));
k.push(B('One curve shifts: both the equilibrium price and quantity are determined. Both curves shift in opposite directions: one of the two is determined and the other is not. Demand right plus supply left pins down a higher price but leaves quantity ambiguous; demand right plus supply right pins down a higher quantity but leaves price ambiguous.'));

k.push(S('§4.5  When Government Dictates the Price'));
k.push(D('Price ceiling','a legal maximum price. Binding only if it is below equilibrium, where it creates a shortage.'));
k.push(D('Price floor','a legal minimum price. Binding only if it is above equilibrium, where it creates a surplus.'));
k.push(B('When price cannot ration the good, something else does — queues, first-come-first-served, favouritism, lotteries. Queuing is the costly one: waiting consumes real hours that benefit nobody. A lottery allocates just as arbitrarily but wastes nothing.'));
k.push(B('A government standing offer to buy unlimited quantity at a fixed price is perfectly elastic demand at that price, and it acts as a floor.'));
k.push(...GT([
  'Demand and supply schedules: find equilibrium, and horizontally sum individual curves into a market curve.',
  'A shift diagram: identify which curve moved, which way, and what happens to equilibrium price and quantity.',
  'A four-panel figure: pick the panel matching a described change.',
  'A binding ceiling or floor: read quantity demanded and quantity supplied off the axis and subtract to get the gap.']));

/* ---------------- CHAPTER 5 ---------------- */
k.push(H('Chapter 5 — Consumers and Incentives'));
k.push(S('§5.1  The Buyer’s Problem'));
k.push(D('Budget set','every bundle the buyer can afford.'));
k.push(D('Budget constraint','the bundles that use up the entire budget — the boundary of the budget set. The set is larger than the constraint.'));
k.push(FM('Budget constraint:  P₁Q₁ + P₂Q₂ = income      Slope (good 1 on the horizontal axis)  =  − P₁ / P₂'));
k.push(B('Income changes shift the constraint in parallel — both intercepts move, the slope does not, because the slope is the price ratio. A change in one price pivots the constraint, changing the slope. A change in income *and* one price does both.'));

k.push(S('§5.2  Putting It All Together'));
k.push(B('An optimizing buyer spends so that the marginal benefit of the last dollar is the same on every good. If one good gave more benefit per dollar, shifting a dollar toward it would raise total benefit — so you would not have been optimizing.'));
k.push(FM('Equal-marginal principle:  MB₁ / P₁  =  MB₂ / P₂  =  …  for every good bought'));
k.push(B('Two consequences worth memorising. If you are told a buyer is optimizing and given the marginal benefit per dollar on one good, it is the same on every other good — the other prices are irrelevant. And if MB per dollar is higher on good A than on good B, shift spending toward A.'));

k.push(S('§5.3  From the Buyer’s Problem to the Demand Curve'));
k.push(B('The demand curve is traced out by solving the buyer’s problem again at every possible price and recording the optimal quantity each time. A price change pivots the budget constraint, moves the optimal bundle, and gives one more point on the demand curve.'));
k.push(B('Market demand is again the horizontal sum across buyers.'));

k.push(S('§5.4  Consumer Surplus'));
k.push(D('Consumer surplus','willingness to pay minus the price actually paid, summed over all units bought. On a graph it is the area below the demand curve and above the market price.'));
k.push(FM('CS on a straight-line demand:  ½ × base × height,  base = quantity bought, height = choke price − market price'));
k.push(B('Because marginal benefit diminishes, each extra unit adds less surplus than the one before. A second identical purchase adds less surplus than the first.'));

k.push(S('§5.5  Demand Elasticities'));
k.push(D('Price elasticity of demand','the responsiveness of quantity demanded to a change in price.'));
k.push(FM('E  =  %ΔQ / %ΔP      Midpoint method: divide each change by the AVERAGE of the old and new values'));
k.push(B('|E| > 1 elastic · |E| < 1 inelastic · |E| = 1 unit elastic · vertical curve is perfectly inelastic (E = 0) · horizontal curve is perfectly elastic.'));
k.push(B('Total-revenue rule. Elastic demand: cutting the price raises total revenue. Inelastic demand: raising the price raises total revenue. Unit elastic: total spending does not change at all — which is the quickest way to spot unit elasticity in a problem.'));
k.push(B('More substitutes, a larger share of the budget, and more time to adjust all make demand more elastic.'));
k.push(FM('Cross-price elasticity  =  %ΔQ of good A / %ΔP of good B      positive → substitutes · negative → complements · zero → unrelated'));
k.push(FM('Income elasticity  =  %ΔQ / %ΔIncome      positive → normal good · negative → inferior good · greater than 1 → luxury'));
k.push(B('To apply an elasticity from a table, multiply: a 10% price rise with a cross-price elasticity of 0.6 changes consumption by 6%, upward because the sign is positive.'));
k.push(...GT([
  'A budget constraint before and after a change: say whether the slope, the position, or both have changed.',
  'A demand curve with a price line: shade and compute consumer surplus, and the change in it when price moves.',
  'A total-benefit table across several goods: find the affordable bundle with the highest total benefit.',
  'Elasticity tables: multiply the elasticity by the percentage change, and read the sign.']));

/* ---------------- CHAPTER 6 ---------------- */
k.push(H('Chapter 6 — Sellers and Incentives'));
k.push(S('§6.1  Sellers in a Perfectly Competitive Market'));
k.push(D('Price taker','a seller too small to affect the market price, who therefore treats it as given.'));
k.push(B('The demand curve facing one firm is horizontal at the market price. The demand curve facing the whole industry slopes downward, because the law of demand holds for the good as a whole. Keep these two apart — it is a standard trap.'));

k.push(S('§6.2  The Seller’s Problem'));
k.push(D('Marginal product','the extra output from one more unit of an input.'));
k.push(D('Specialization','the range over which marginal product is RISING as workers are added.'));
k.push(D('Diminishing returns','the range over which marginal product is FALLING but still positive.'));
k.push(B('Beyond that, marginal product turns negative and total output falls — that is a third region, not part of diminishing returns. Distinguishing the two boundaries from a total-output column is directly tested.'));
k.push(D('Explicit cost','a direct monetary payment. Implicit cost — the opportunity cost of a resource you already own, such as the owner’s own time or capital.'));
k.push(FM('Accounting profit  =  TR − explicit costs      Economic profit  =  TR − explicit costs − implicit costs'));
k.push(B('Economic profit is therefore never larger than accounting profit. A firm earning zero economic profit still shows a positive accounting profit.'));
k.push(FM('AFC = FC/Q · AVC = VC/Q · ATC = TC/Q = AFC + AVC · MC = ΔTC/ΔQ · Profit = (P − ATC) × Q'));
k.push(B('Fixed cost can be read off a cost graph as the gap between ATC and AVC multiplied by quantity. MC cuts both AVC and ATC at their minimum points, from below.'));
k.push(D('Economies of scale','average cost falls as output rises. Specialization — each worker doing what they are best at — is one of its sources.'));

k.push(S('§6.3  From the Seller’s Problem to the Supply Curve'));
k.push(B('A price-taking firm produces the quantity at which price equals marginal cost — that is, every unit whose marginal cost does not exceed the price.'));
k.push(FM('Profit-maximizing output:  P = MC      Firm’s short-run supply curve: the MC curve at every price at or above minimum AVC'));
k.push(D('Price elasticity of supply','%ΔQ supplied / %ΔP. A supply curve is unit-elastic when it is a straight line through the origin — whatever its slope. Elasticity and slope are not the same thing.'));

k.push(S('§6.4  Producer Surplus'));
k.push(D('Producer surplus','the price received minus the seller’s willingness to accept, summed over the units sold. On a graph it is the area above the supply curve and below the market price.'));
k.push(B('Producer surplus is not profit. It subtracts variable costs only; profit also subtracts fixed costs.'));
k.push(FM('PS on a straight-line supply:  ½ × base × height,  base = quantity sold, height = price − the supply curve’s intercept'));

k.push(S('§6.5  From the Short Run to the Long Run'));
k.push(B('In the short run at least one input is fixed, so fixed costs must be paid whether or not the firm produces. In the long run everything is adjustable and the firm can leave the industry entirely.'));
k.push(FM('Shut down (short run) if  P < minimum AVC       Exit (long run) if  P < minimum ATC'));
k.push(B('A firm that shuts down still pays its fixed cost; a firm that exits no longer has one. So a firm losing money can be right to keep producing: if price covers average variable cost, every unit sold contributes something toward the fixed cost, and the loss is smaller than it would be at zero output. Compare the two losses rather than reasoning from the sign of profit.'));

k.push(S('§6.6  Long-Run Competitive Equilibrium'));
k.push(B('Economic profits attract entry, which shifts market supply right and pushes the price down. Losses cause exit, which shifts supply left and pushes the price up. Entry and exit continue until economic profit is exactly zero.'));
k.push(FM('Long-run equilibrium:  P = minimum ATC  and  economic profit = 0'));
k.push(...GT([
  'A cost-curve diagram with MC, AVC, ATC and MR: locate the profit-maximizing quantity, the shutdown point, the break-even point, and read fixed cost, profit or loss as an area.',
  'A total-output table: compute marginal product and mark where specialization ends and diminishing returns begin.',
  'A supply schedule for two firms: sum horizontally and read a firm’s willingness to accept for a given unit.',
  'A supply curve with a price line: shade and compute producer surplus, and its change when price moves.',
  'An industry diagram with entry or exit: say which curve moves, which way, and where the process stops.']));

/* ---------------- FORMULAS ---------------- */
k.push(H('Key Formulas'));
[ 'Net benefit = total benefit − total cost',
  'Optimum at the margin: expand while MB ≥ MC; optimum where MB = MC',
  'Opportunity cost of time = hours × value per hour (use the wage when one is given)',
  'Budget constraint: P₁Q₁ + P₂Q₂ = income;  slope = − P₁/P₂',
  'Equal-marginal principle: MB₁/P₁ = MB₂/P₂ for every good purchased',
  'Consumer surplus = willingness to pay − price paid (area below D, above P)',
  'Producer surplus = price − willingness to accept (area above S, below P)',
  'Area of a triangle = ½ × base × height;  area of a rectangle = base × height',
  'Elasticity = %ΔQ / %ΔP, using the midpoint (average) as the base',
  'Cross-price elasticity = %ΔQ_A / %ΔP_B;  income elasticity = %ΔQ / %ΔIncome',
  'Market demand or supply = horizontal sum of the individual curves',
  'Accounting profit = TR − explicit costs;  economic profit = TR − explicit − implicit',
  'MC = ΔTC/ΔQ · AVC = VC/Q · ATC = TC/Q · AFC = FC/Q',
  'Fixed cost = (ATC − AVC) × Q',
  'Profit = (P − ATC) × Q',
  'Marginal product = ΔOutput / ΔInput',
  'Firm supply: P = MC, for prices at or above minimum AVC',
  'Shut down if P < min AVC;  exit if P < min ATC',
  'Long-run competitive equilibrium: P = min ATC, economic profit = 0'
].forEach(x=>k.push(L(x)));

const doc=new Document({
  numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:400,hanging:200}}}}]}]},
  styles:{default:{document:{run:{font:F,size:22,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1150,bottom:1150,left:1150,right:1150}}},children:k}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('ECON003_Midterm_Study_Guide.docx',b);console.log('written',b.length);});
