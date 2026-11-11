const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,LevelFormat,AlignmentType,ShadingType}=require('docx');
const NAVY='1A365D', INK='222222', ACC='B45F06', F='等线';
const t=(x,o={})=>new TextRun({text:x,font:F,...o});
const p=o=>new Paragraph(o);
const H=x=>p({heading:HeadingLevel.HEADING_1,spacing:{before:320,after:110},children:[t(x,{bold:true,size:32,color:NAVY})]});
const S=x=>p({spacing:{before:170,after:60},children:[t(x,{bold:true,size:23,color:NAVY})]});
const B=x=>p({spacing:{after:64},children:[t(x,{size:22,color:INK})]});
const D=(a,b)=>p({spacing:{after:64},children:[t(a+' — ',{bold:true,size:22,color:INK}),t(b,{size:22,color:INK})]});
const L=x=>p({numbering:{reference:'b',level:0},spacing:{after:48},children:[t(x,{size:22,color:INK})]});
const Lb=(a,b)=>p({numbering:{reference:'b',level:0},spacing:{after:48},children:[t(a+' — ',{bold:true,size:22,color:INK}),t(b,{size:22,color:INK})]});
const FM=x=>p({spacing:{after:56},indent:{left:280},shading:{type:ShadingType.CLEAR,fill:'F2F5FA'},children:[t('  '+x+'  ',{size:22,bold:true,color:NAVY})]});
// Wording-to-watch box: a distinction the exam phrases turn on.
const W=(head,body)=>p({spacing:{before:80,after:80},indent:{left:280},shading:{type:ShadingType.CLEAR,fill:'FFF4E5'},
  children:[t('  '+head+' — ',{size:22,bold:true,color:ACC}),t(body+'  ',{size:22,color:INK})]});
const GT=(ls)=>[p({spacing:{before:120,after:50},children:[t('Graphs and Tables',{bold:true,size:21,color:ACC})]})]
  .concat(ls.map(x=>p({numbering:{reference:'b',level:0},spacing:{after:44},children:[t(x,{size:21,color:INK})]})));
const k=[];
k.push(p({spacing:{after:36},children:[t('ECON 003',{bold:true,size:56,color:NAVY})]}));
k.push(p({spacing:{after:110},children:[t('Midterm Exam Study Guide',{bold:true,size:40,color:NAVY})]}));
k.push(p({spacing:{after:36},children:[t('Saturday, August 15, 2026  |  10:00 AM – 12:00 PM (Pacific)',{size:23,color:INK})]}));
k.push(p({spacing:{after:36},children:[t('50 multiple-choice questions, drawn at random  |  Chapters 1, 3, 4, 5, 6',{size:23,color:INK})]}));
k.push(p({spacing:{after:220},border:{bottom:{style:BorderStyle.SINGLE,size:10,color:NAVY}},children:[t('')]}));

k.push(H('Key Notation'));
[['P','price'],['Q','quantity'],['QD','quantity demanded'],['QS','quantity supplied'],
 ['D, S','demand curve, supply curve'],['WTP','willingness to pay'],['WTA','willingness to accept'],
 ['MB','marginal benefit'],['MC','marginal cost'],['MR','marginal revenue'],['MP','marginal product'],
 ['TB, TC','total benefit, total cost'],['TR','total revenue'],['FC, VC','fixed cost, variable cost'],
 ['AFC, AVC, ATC','average fixed, average variable, average total cost'],['LRATC','long-run average total cost'],
 ['CS, PS','consumer surplus, producer surplus'],['E','elasticity'],['SR, LR','short run, long run'],['Δ','change in']
].forEach(([a,b])=>k.push(Lb(a,b)));

k.push(H('Chapter 1 — The Principles and Practice of Economics'));
k.push(S('§1.1  The Scope of Economics'));
k.push(D('Economics','the study of how agents choose to allocate scarce resources.'));
k.push(D('Scarce resources','resources of limited supply; using them one way forecloses another.'));
k.push(D('Economic agent','an individual or group that makes choices.'));
k.push(D('Microeconomics','individuals, households, firms, and single markets.'));
k.push(D('Macroeconomics','the economy as a whole — growth, unemployment, inflation.'));
k.push(D('Model','a simplified description of reality used to make predictions.'));
k.push(S('§1.2  Three Principles of Economics'));
k.push(Lb('Optimization','choosing the best feasible option.'));
k.push(Lb('Equilibrium','a situation in which nobody would benefit by changing their own behavior.'));
k.push(Lb('Empiricism','analysis that uses data to test theories and identify causes.'));
k.push(S('§1.3  The First Principle: Optimization'));
k.push(D('Trade-off','more of one thing means less of another.'));
k.push(D('Opportunity cost','the value of the best alternative given up.'));
k.push(D('Budget constraint','the choices that exactly exhaust available resources.'));
k.push(B('Optimization is an approximation of actual behavior, not a claim that choices are perfect.'));
k.push(S('§1.4  The Second Principle: Equilibrium'));
k.push(B('In equilibrium: quantity demanded equals quantity supplied; sellers’ costs are covered by the price; buyers value the good at least at the price.'));
k.push(B('In equilibrium neither side gains by changing its own behavior.'));
k.push(D('Free riding','enjoying a benefit that cannot be withheld, without contributing to its cost.'));
k.push(S('§1.5  The Third Principle: Empiricism'));
k.push(D('Positive analysis','what is; testable against evidence.'));
k.push(D('Normative analysis','what ought to be; rests on a value judgment.'));
k.push(B('Optimization is used both positively and normatively.'));
k.push(B('Correlation is not causation.'));

k.push(H('Chapter 3 — Optimization'));
k.push(S('§3.1  Choosing the Best Feasible Option'));
k.push(D('Feasible option','affordable and achievable given the constraints.'));
k.push(D('Net benefit','total benefit minus total cost.'));
k.push(FM('Net benefit  =  total benefit  −  total cost'));
k.push(B('The optimum is the feasible option with the highest net benefit. Feasibility is checked before ranking.'));
k.push(S('§3.2  Optimization Using Total Value (in Levels)'));
k.push(B('Compute the total value or total cost of each whole option and compare directly.'));
k.push(B('Where one cost falls as another rises, the optimum minimizes their sum, not either cost alone.'));
k.push(B('Time is costed at the value of its next-best use, usually the wage. A higher value of time raises the cost of every time-consuming option.'));
k.push(FM('Total cost  =  money cost  +  (hours × value per hour)'));
k.push(S('§3.3  Optimization Using Marginal Analysis (in Differences)'));
k.push(D('Marginal benefit','the additional benefit from one more unit.'));
k.push(D('Marginal cost','the additional cost from one more unit.'));
k.push(FM('Expand while  MB ≥ MC.   Optimum where  MB = MC'));
k.push(B('Optimization in levels and optimization in differences give identical answers.'));
k.push(D('Marginal versus average','marginal is the value of one more unit; average is value per unit across all units.'));
k.push(...GT(['Total-benefit or net-benefit column: difference consecutive rows for marginal values.',
 'Marginal benefit and marginal cost table: the last row where MB ≥ MC.',
 'Marginal benefit bars against a flat marginal cost: the crossing point.']));

k.push(H('Chapter 4 — Demand, Supply, and Equilibrium'));
k.push(S('§4.1  Markets'));
k.push(D('Market','a group of agents trading a good or service, plus the rules and arrangements for trading.'));
k.push(D('Perfectly competitive market','sellers trade identical goods; no individual buyer or seller is large enough to affect the market price; entry and exit are free.'));
k.push(D('Price taker','accepts the market price as given; faces a flat demand curve.'));
k.push(D('Price maker','can influence the price; faces a downward-sloping demand curve.'));
k.push(D('Ceteris paribus','holding all else equal.'));
k.push(S('§4.2  How Buyers Behave'));
k.push(D('Demand schedule','a table of quantity demanded at each price.'));
k.push(D('Demand curve','the plot of that schedule; downward sloping.'));
k.push(D('Law of demand','quantity demanded rises when price falls, ceteris paribus.'));
k.push(D('Willingness to pay','the most a buyer will pay for a unit.'));
k.push(D('Diminishing marginal benefit','each additional unit is worth less than the one before.'));
k.push(B('Market demand is the horizontal sum of individual demand curves: at a fixed price, add the quantities.'));
k.push(B('A change in the good’s own price is a movement along the curve. Every other change shifts it.'));
k.push(W('Watch the wording','these two phrases are not interchangeable, and questions are written to separate them. A change in QUANTITY DEMANDED is a movement along a demand curve that has not moved; only the good’s own price causes it. A change in DEMAND is a shift of the whole curve to a new position; only the five shifters below cause it, never the good’s own price. So “demand fell” means the curve moved left; “quantity demanded fell” means buyers slid up the same curve. If a question names a cause, decide first which of the two it is — the rest of the answer follows.'));
k.push(Lb('Five demand shifters','tastes and preferences; income and wealth; price and availability of related goods; number and scale of buyers; beliefs about the future.'));
k.push(B('Substitutes: price of one rises, demand for the other rises. Complements: price of one rises, demand for the other falls.'));
k.push(B('Normal good: income rises, demand rises. Inferior good: income rises, demand falls.'));
k.push(S('§4.3  How Sellers Behave'));
k.push(D('Supply schedule','a table of quantity supplied at each price.'));
k.push(D('Supply curve','the plot of that schedule; upward sloping.'));
k.push(D('Law of supply','quantity supplied rises when price rises, ceteris paribus.'));
k.push(D('Willingness to accept','the least a seller will accept for a unit; equal to the marginal cost of that unit.'));
k.push(B('Market supply is the horizontal sum of individual supply curves.'));
k.push(Lb('Four supply shifters','prices of inputs; technology; number and scale of sellers; beliefs about the future.'));
k.push(B('A change in the good’s own price is a movement along the curve. Every other change shifts it.'));
k.push(W('Watch the wording','the supply side works the same way. A change in QUANTITY SUPPLIED is a movement along a supply curve that has not moved, caused only by the good’s own price. A change in SUPPLY is a shift of the curve, caused only by the four shifters above. A rise in the wage sellers pay shifts supply; a rise in the price of the good itself does not.'));
k.push(S('§4.4  Supply and Demand in Equilibrium'));
k.push(D('Competitive equilibrium','the price at which quantity demanded equals quantity supplied.'));
k.push(D('Excess demand (shortage)','quantity demanded exceeds quantity supplied; occurs below the equilibrium price.'));
k.push(D('Excess supply (surplus)','quantity supplied exceeds quantity demanded; occurs above the equilibrium price.'));
k.push(B('On a graph, a shortage or surplus is the horizontal gap between the two curves at the stated price.'));
k.push(B('One curve shifts: equilibrium price and quantity are both determined.'));
k.push(B('Both curves shift in opposite directions: one of the two is determined, the other is ambiguous.'));
k.push(S('§4.5  When Government Dictates the Price'));
k.push(D('Price ceiling','a legal maximum price; binding below equilibrium; creates a shortage.'));
k.push(D('Price floor','a legal minimum price; binding above equilibrium; creates a surplus.'));
k.push(D('Non-price rationing','allocation by queues, first-come-first-served, favoritism, or lottery when price cannot clear the market.'));
k.push(B('An unlimited government offer to buy at a fixed price is perfectly elastic demand at that price and acts as a floor.'));
k.push(...GT(['Demand and supply schedules: equilibrium, and horizontal summation into market curves.',
 'Shift diagram: which curve moved, which way, and the effect on equilibrium price and quantity.',
 'Binding ceiling or floor: quantity demanded and quantity supplied at the controlled price, and the gap between them.']));

k.push(H('Chapter 5 — Consumers and Incentives'));
k.push(S('§5.1  The Buyer’s Problem'));
k.push(B('The buyer’s problem has three parts: tastes and preferences, prices, and the budget.'));
k.push(D('Budget set','every bundle the buyer can afford.'));
k.push(D('Budget constraint','the bundles that exhaust the budget; the boundary of the budget set. The set is larger than the constraint.'));
k.push(FM('P₁Q₁ + P₂Q₂ = income      Slope (good 1 on the horizontal axis)  =  − P₁ / P₂'));
k.push(B('An income change shifts the constraint in parallel. A change in one price pivots it and changes the slope.'));
k.push(S('§5.2  Putting It All Together'));
k.push(B('An optimizing buyer equates the marginal benefit of the last dollar across every good purchased.'));
k.push(FM('MB₁ / P₁  =  MB₂ / P₂  =  …  for every good bought'));
k.push(B('Marginal utility is the same idea as marginal benefit.'));
k.push(B('If marginal benefit per dollar is higher on one good, spending shifts toward it.'));
k.push(S('§5.3  From the Buyer’s Problem to the Demand Curve'));
k.push(B('The demand curve is traced by solving the buyer’s problem at each price and recording the optimal quantity.'));
k.push(B('A price change pivots the budget constraint and moves the optimal bundle.'));
k.push(B('Market demand is the horizontal sum across buyers.'));
k.push(S('§5.4  Consumer Surplus'));
k.push(D('Consumer surplus','willingness to pay minus price paid, summed over the units bought; the area below the demand curve and above the market price.'));
k.push(FM('CS on a straight-line demand:  ½ × base × height,  base = quantity, height = choke price − market price'));
k.push(B('Because marginal benefit diminishes, each additional unit adds less surplus than the one before.'));
k.push(S('§5.5  Demand Elasticities'));
k.push(D('Price elasticity of demand','the responsiveness of quantity demanded to a change in price.'));
k.push(FM('E  =  %ΔQ / %ΔP      Midpoint method: each change divided by the average of the old and new values'));
k.push(B('|E| > 1 elastic · |E| < 1 inelastic · |E| = 1 unit elastic · vertical curve perfectly inelastic · horizontal curve perfectly elastic.'));
k.push(B('Total revenue: elastic demand, a price cut raises revenue; inelastic demand, a price rise raises revenue; unit elastic, total spending is unchanged.'));
k.push(B('Demand is more elastic with more substitutes, a larger share of the budget, and more time to adjust.'));
k.push(FM('Cross-price elasticity  =  %ΔQ of A / %ΔP of B      positive → substitutes · negative → complements · zero → unrelated'));
k.push(FM('Income elasticity  =  %ΔQ / %Δincome      negative → inferior · between 0 and 1 → normal necessity · above 1 → normal luxury'));
k.push(...GT(['Budget constraint before and after a change: slope, position, or both.',
 'Demand curve with a price line: consumer surplus as an area, and its change when price moves.',
 'Total-benefit table across goods: the affordable bundle with the highest total benefit.',
 'Elasticity table: the elasticity multiplied by the percentage change, and the sign.']));

k.push(H('Chapter 6 — Sellers and Incentives'));
k.push(S('§6.1  Sellers in a Perfectly Competitive Market'));
k.push(B('Conditions: sellers produce identical goods; no buyer or seller is large enough to influence the market price; there is free entry and exit.'));
k.push(D('Free entry','entry unobstructed by legal or technical barriers.'));
k.push(D('Price taker','a seller too small to affect the market price.'));
k.push(B('An individual firm faces a horizontal demand curve at the market price. The industry faces a downward-sloping demand curve.'));
k.push(S('§6.2  The Seller’s Problem'));
k.push(B('The seller’s problem has three parts: production, costs, and revenues.'));
k.push(D('Production function','the relationship between inputs and the output they produce.'));
k.push(D('Marginal product','the additional output from one more unit of an input.'));
k.push(D('Specialization','the range over which marginal product is rising.'));
k.push(D('Diminishing returns','the range over which marginal product is falling but still positive.'));
k.push(B('Beyond that range marginal product is negative and total output falls.'));
k.push(D('Fixed cost','does not vary with output. Variable cost — varies with output.'));
k.push(D('Sunk cost','a cost already committed that can never be recovered; irrelevant to current decisions. Fixed costs are sunk in the short run.'));
k.push(D('Explicit cost','a direct monetary payment. Implicit cost — the opportunity cost of a resource already owned.'));
k.push(FM('Accounting profit = TR − explicit costs      Economic profit = TR − explicit costs − implicit costs'));
k.push(B('Economic profit is never larger than accounting profit. Zero economic profit means positive accounting profit.'));
k.push(FM('AFC = FC/Q · AVC = VC/Q · ATC = TC/Q = AFC + AVC · MC = ΔTC/ΔQ · Profit = (P − ATC) × Q'));
k.push(B('MC cuts AVC and ATC at their minimum points, from below. Fixed cost is the gap between ATC and AVC multiplied by quantity.'));
k.push(D('Economies of scale','LRATC falls as output rises. Constant returns to scale — LRATC is flat. Diseconomies of scale — LRATC rises.'));
k.push(B('Specialization is one source of economies of scale.'));
k.push(S('§6.3  From the Seller’s Problem to the Supply Curve'));
k.push(FM('Profit-maximizing output:  P = MC      Firm’s short-run supply curve: MC at every price at or above minimum AVC'));
k.push(D('Price elasticity of supply','%ΔQ supplied / %ΔP; positive, because a higher price raises quantity supplied.'));
k.push(B('A supply curve is unit-elastic when it is a straight line through the origin, whatever its slope. Elasticity and slope are different properties.'));
k.push(B('Supply is more elastic with more time to adjust and more spare capacity.'));
k.push(S('§6.4  Producer Surplus'));
k.push(D('Producer surplus','price received minus willingness to accept, summed over the units sold; the area above the supply curve and below the market price.'));
k.push(B('Producer surplus is not profit: it subtracts variable costs only, while profit also subtracts fixed costs.'));
k.push(FM('PS on a straight-line supply:  ½ × base × height,  base = quantity sold, height = price − supply intercept'));
k.push(S('§6.5  From the Short Run to the Long Run'));
k.push(B('Short run: at least one input is fixed, and fixed costs are paid whether or not the firm produces.'));
k.push(B('Long run: every input is adjustable and the firm may leave the industry.'));
k.push(FM('Shut down (short run) if  P < minimum AVC      Exit (long run) if  P < minimum ATC'));
k.push(B('A firm that shuts down still pays its fixed cost. A firm that exits does not.'));
k.push(S('§6.6  Long-Run Competitive Equilibrium'));
k.push(B('Economic profits attract entry, shifting market supply right and lowering the price.'));
k.push(B('Losses cause exit, shifting market supply left and raising the price.'));
k.push(FM('Long-run equilibrium:  P = minimum ATC  and  economic profit = 0'));
k.push(...GT(['Cost-curve diagram with MC, AVC, ATC and MR: profit-maximizing quantity, shutdown point, break-even point, and fixed cost, profit or loss as an area.',
 'Total-output table: marginal product, and the boundaries between specialization, diminishing returns, and negative returns.',
 'Supply schedules for individual firms: horizontal summation, and willingness to accept for a given unit.',
 'Supply curve with a price line: producer surplus as an area, and its change when price moves.',
 'Industry diagram with entry or exit: which curve moves, which way, and where the process stops.',
 'LRATC curve: economies of scale, constant returns to scale, diseconomies of scale.']));

k.push(H('Key Formulas'));
['Net benefit = total benefit − total cost',
 'Optimum at the margin: expand while MB ≥ MC; optimum where MB = MC',
 'Opportunity cost of time = hours × value per hour',
 'Budget constraint: P₁Q₁ + P₂Q₂ = income; slope = − P₁/P₂',
 'Equal-marginal principle: MB₁/P₁ = MB₂/P₂ for every good bought',
 'Consumer surplus = willingness to pay − price paid',
 'Producer surplus = price − willingness to accept',
 'Triangle = ½ × base × height · rectangle = base × height',
 'Price elasticity = %ΔQ / %ΔP, midpoint base = average of old and new',
 'Cross-price elasticity = %ΔQ_A / %ΔP_B · income elasticity = %ΔQ / %Δincome',
 'Market demand or supply = horizontal sum of individual curves',
 'Accounting profit = TR − explicit · economic profit = TR − explicit − implicit',
 'MC = ΔTC/ΔQ · AVC = VC/Q · ATC = TC/Q · AFC = FC/Q',
 'Fixed cost = (ATC − AVC) × Q',
 'Profit = (P − ATC) × Q',
 'Marginal product = Δoutput / Δinput',
 'Firm supply: P = MC at prices at or above minimum AVC',
 'Shut down if P < min AVC · exit if P < min ATC',
 'Long-run equilibrium: P = min ATC, economic profit = 0'
].forEach(x=>k.push(L(x)));

const doc=new Document({
  numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:400,hanging:200}}}}]}]},
  styles:{default:{document:{run:{font:F,size:22,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1150,bottom:1150,left:1150,right:1150}}},children:k}]});
const {writeVersioned}=require('./ver.js');
Packer.toBuffer(doc).then(b=>{const o=writeVersioned('ECON003_Midterm_Study_Guide',b);
  console.log('->',o.name,'|',b.length,'bytes');});
