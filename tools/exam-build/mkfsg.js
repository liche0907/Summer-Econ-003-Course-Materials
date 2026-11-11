const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,LevelFormat,AlignmentType,ShadingType}=require('docx');
const NAVY='1A365D', INK='222222', ACC='B45F06', F='等线';
const t=(x,o={})=>new TextRun({text:x,font:F,...o});
const p=o=>new Paragraph(o);
const H=x=>p({heading:HeadingLevel.HEADING_1,spacing:{before:320,after:110},children:[t(x,{bold:true,size:32,color:NAVY})]});
const PART=x=>p({spacing:{before:400,after:150},border:{bottom:{style:BorderStyle.SINGLE,size:8,color:NAVY}},
  children:[t(x,{bold:true,size:28,color:NAVY,allCaps:true})]});
const S=x=>p({spacing:{before:170,after:60},children:[t(x,{bold:true,size:23,color:NAVY})]});
const B=x=>p({spacing:{after:64},children:[t(x,{size:22,color:INK})]});
const D=(a,b)=>p({spacing:{after:64},children:[t(a+' — ',{bold:true,size:22,color:INK}),t(b,{size:22,color:INK})]});
const L=x=>p({numbering:{reference:'b',level:0},spacing:{after:48},children:[t(x,{size:22,color:INK})]});
const Lb=(a,b)=>p({numbering:{reference:'b',level:0},spacing:{after:48},children:[t(a+' — ',{bold:true,size:22,color:INK}),t(b,{size:22,color:INK})]});
const FM=(...xs)=>xs.map((x,i)=>p({spacing:{before:i===0?40:0,after:i===xs.length-1?60:0,line:280},indent:{left:280},shading:{type:ShadingType.CLEAR,fill:'F2F5FA'},children:[t('  '+x+'  ',{size:22,bold:true,color:NAVY})]}));
const W=(head,body)=>p({spacing:{before:80,after:80},indent:{left:280},shading:{type:ShadingType.CLEAR,fill:'FFF4E5'},
  children:[t('  '+head+' — ',{size:22,bold:true,color:ACC}),t(body+'  ',{size:22,color:INK})]});
const GT=(ls)=>[p({spacing:{before:120,after:50},children:[t('Graphs and Tables',{bold:true,size:21,color:ACC})]})]
  .concat(ls.map(x=>p({numbering:{reference:'b',level:0},spacing:{after:44},children:[t(x,{size:21,color:INK})]})));
const k=[];
const push=(...xs)=>xs.forEach(x=>Array.isArray(x)?x.forEach(y=>k.push(y)):k.push(x));

/* ─────────── COVER ─────────── */
push(p({spacing:{after:36},children:[t('ECON 003',{bold:true,size:56,color:NAVY})]}));
push(p({spacing:{after:110},children:[t('Final Exam Study Guide',{bold:true,size:40,color:NAVY})]}));
push(p({spacing:{after:36},children:[t('Saturday, August 29, 2026  |  10:00 AM – 1:00 PM (Pacific)',{size:23,color:INK})]}));
push(p({spacing:{after:36},children:[t('Cumulative  |  Chapters 1, 3, 4, 5, 6, 7, 8, 9, 10, 12',{size:23,color:INK})]}));
push(p({spacing:{after:220},border:{bottom:{style:BorderStyle.SINGLE,size:10,color:NAVY}},children:[t('')]}));

push(H('Coverage'));
push(S('Covered'));
push(Lb('Chapters 1, 3, 4, 5, 6','all sections.'));
push(Lb('Chapter 7','§7.1, §7.3, §7.4, §7.5.'));
push(Lb('Chapter 8','§8.1 – §8.5.'));
push(Lb('Chapter 9','§9.1 – §9.5.'));
push(Lb('Chapter 10','§10.1.3, §10.2, §10.3.'));
push(Lb('Chapter 12','§12.1 – §12.5.'));
push(S('Not covered'));
push(Lb('Chapters 2 and 11','not lectured.'));
push(Lb('§7.2  From the Individual to the Firm','not lectured.'));
push(Lb('§10.1.1 and §10.1.2','levels of government, the deficit, tax brackets, progressive against regressive structures. Not lectured — no average or marginal tax rate arithmetic.'));
push(Lb('§10.4 and §10.5','equity against efficiency is covered under §7.5; paternalism was not lectured.'));
push(Lb('§12.6  Price discrimination','not lectured.'));
push(Lb('§12.7  Regulation of monopoly, antitrust','lectured, but not assessed.'));

/* ─────────── NOTATION ─────────── */
push(H('Key Notation'));
[['P','price'],['Q','quantity'],['QD','quantity demanded'],['QS','quantity supplied'],
 ['D, S','demand curve, supply curve'],['WTP','willingness to pay'],['WTA','willingness to accept'],
 ['MB','marginal benefit'],['MC','marginal cost'],['MR','marginal revenue'],['MP','marginal product'],
 ['TB, TC','total benefit, total cost'],['TR','total revenue'],['FC, VC','fixed cost, variable cost'],
 ['AFC, AVC, ATC','average fixed, average variable, average total cost'],['LRATC','long-run average total cost'],
 ['CS, PS','consumer surplus, producer surplus'],['TS','total surplus, also called social surplus'],
 ['DWL','deadweight loss'],['PPC','production possibilities curve'],
 ['MSC','marginal social cost'],
 ['MSB','marginal social benefit'],
 ['E','elasticity'],['SR, LR','short run, long run'],['Δ','change in']
].forEach(([a,b])=>push(Lb(a,b)));

/* ═══════ PART ONE ═══════ */
push(PART('Part One  ·  Chapters 1, 3, 4, 5, 6'));

push(H('Chapter 1 — The Principles and Practice of Economics'));
push(S('§1.1  The Scope of Economics'));
push(D('Economics','the study of how agents choose to allocate scarce resources.'));
push(D('Scarce resources','resources of limited supply; using them one way forecloses another.'));
push(D('Economic agent','an individual or group that makes choices.'));
push(D('Microeconomics','individuals, households, firms, and single markets.'));
push(D('Macroeconomics','the economy as a whole — growth, unemployment, inflation.'));
push(D('Model','a simplified description of reality used to make predictions.'));
push(S('§1.2  Three Principles of Economics'));
push(Lb('Optimization','choosing the best feasible option.'));
push(Lb('Equilibrium','a situation in which nobody would benefit by changing their own behavior.'));
push(Lb('Empiricism','analysis that uses data to test theories and identify causes.'));
push(S('§1.3  The First Principle: Optimization'));
push(D('Trade-off','more of one thing means less of another.'));
push(D('Opportunity cost','the value of the best alternative given up.'));
push(D('Budget constraint','the choices that exactly exhaust available resources.'));
push(B('Optimization is an approximation of actual behavior, not a claim that choices are perfect.'));
push(S('§1.4  The Second Principle: Equilibrium'));
push(B('In equilibrium: quantity demanded equals quantity supplied; sellers’ costs are covered by the price; buyers value the good at least at the price.'));
push(B('In equilibrium neither side gains by changing its own behavior.'));
push(D('Free riding','enjoying a benefit that cannot be withheld, without contributing to its cost.'));
push(S('§1.5  The Third Principle: Empiricism'));
push(D('Positive analysis','what is; testable against evidence.'));
push(D('Normative analysis','what ought to be; rests on a value judgment.'));
push(B('Optimization is used both positively and normatively.'));
push(B('Correlation is not causation.'));

push(H('Chapter 3 — Optimization'));
push(S('§3.1  Choosing the Best Feasible Option'));
push(D('Feasible option','affordable and achievable given the constraints.'));
push(D('Net benefit','total benefit minus total cost.'));
push(FM('Net benefit  =  total benefit  −  total cost'));
push(B('The optimum is the feasible option with the highest net benefit. Feasibility is checked before ranking.'));
push(S('§3.2  Optimization Using Total Value (in Levels)'));
push(B('The total value or total cost of each whole option is computed and the options compared directly.'));
push(B('Time is costed at the value of its next-best use, usually the wage.'));
push(S('§3.3  Optimization Using Marginal Analysis (in Differences)'));
push(D('Marginal benefit','the additional benefit from one more unit.'));
push(D('Marginal cost','the additional cost from one more unit.'));
push(FM('Expand while  MB ≥ MC','Optimum where  MB = MC'));
push(B('Optimization in levels and optimization in differences give identical answers.'));
push(W('Marginal and average','marginal is the value of one more unit; average is value per unit across all units.'));
push(GT([
 'Total-benefit or net-benefit column: difference consecutive rows for marginal values.',
 'Marginal benefit and marginal cost table: the last row where MB ≥ MC.',
 'Marginal benefit bars against a flat marginal cost: the crossing point.']));

push(H('Chapter 4 — Demand, Supply, and Equilibrium'));
push(S('§4.1  Markets'));
push(D('Market','a group of agents trading a good or service, plus the rules and arrangements for trading.'));
push(D('Perfectly competitive market','sellers trade identical goods; no individual buyer or seller is large enough to affect the market price; entry and exit are free.'));
push(D('Price taker','accepts the market price as given; faces a flat demand curve.'));
push(D('Price maker','can influence the price; faces a downward-sloping demand curve.'));
push(D('Ceteris paribus','holding all else equal.'));
push(S('§4.2  How Buyers Behave'));
push(D('Demand schedule','a table of quantity demanded at each price.'));
push(D('Demand curve','the plot of that schedule; downward sloping.'));
push(D('Law of demand','quantity demanded rises when price falls, ceteris paribus.'));
push(D('Willingness to pay','the most a buyer will pay for a unit.'));
push(D('Diminishing marginal benefit','each additional unit is worth less than the one before.'));
push(B('Market demand is the horizontal sum of individual demand curves: at a fixed price, add the quantities.'));
push(W('Movement and shift','a change in the good’s own price is a movement along the curve; every other change shifts the curve.'));
push(L('Five demand shifters — tastes and preferences; income and wealth; price and availability of related goods; number and scale of buyers; beliefs about the future.'));
push(B('Substitutes: price of one rises, demand for the other rises. Complements: price of one rises, demand for the other falls.'));
push(B('Normal good: income rises, demand rises. Inferior good: income rises, demand falls.'));
push(S('§4.3  How Sellers Behave'));
push(D('Supply schedule','a table of quantity supplied at each price.'));
push(D('Supply curve','the plot of that schedule; upward sloping.'));
push(D('Law of supply','quantity supplied rises when price rises, ceteris paribus.'));
push(D('Willingness to accept','the least a seller will accept for a unit; equal to the marginal cost of that unit.'));
push(B('Market supply is the horizontal sum of individual supply curves.'));
push(L('Four supply shifters — prices of inputs; technology; number and scale of sellers; beliefs about the future.'));
push(S('§4.4  Supply and Demand in Equilibrium'));
push(D('Competitive equilibrium','the price at which quantity demanded equals quantity supplied.'));
push(D('Excess demand (shortage)','quantity demanded exceeds quantity supplied; occurs below the equilibrium price.'));
push(D('Excess supply (surplus)','quantity supplied exceeds quantity demanded; occurs above the equilibrium price.'));
push(B('One curve shifts: equilibrium price and quantity are both determined.'));
push(B('Both curves shift in opposite directions: one of the two is determined, the other is ambiguous.'));
push(S('§4.5  When Government Dictates the Price'));
push(D('Price ceiling','a legal maximum price; binding below equilibrium; creates a shortage.'));
push(D('Price floor','a legal minimum price; binding above equilibrium; creates a surplus.'));
push(D('Non-price rationing','allocation by queues, first-come-first-served, favoritism, or lottery when price cannot clear the market.'));
push(W('Binding and non-binding','a ceiling above the equilibrium price, or a floor below it, has no effect.'));
push(GT([
 'Demand and supply schedules: equilibrium, and horizontal summation into market curves.',
 'Shift diagram: which curve moved, which way, and the effect on equilibrium price and quantity.',
 'Binding ceiling or floor: quantity demanded and quantity supplied at the controlled price, and the gap between them.']));

push(H('Chapter 5 — Consumers and Incentives'));
push(S('§5.1  The Buyer’s Problem'));
push(B('The buyer’s problem has three parts: tastes and preferences, prices, and the budget.'));
push(D('Budget set','every bundle the buyer can afford.'));
push(D('Budget constraint','the bundles that exhaust the budget; the boundary of the budget set. The set is larger than the constraint.'));
push(FM('P₁Q₁ + P₂Q₂  =  income','Slope, good 1 on the horizontal axis  =  − P₁ / P₂'));
push(B('An income change shifts the constraint in parallel. A change in one price pivots it and changes the slope.'));
push(S('§5.2  Putting It All Together'));
push(B('An optimizing buyer equates the marginal benefit of the last dollar across every good purchased.'));
push(FM('MB₁ / P₁  =  MB₂ / P₂  =  …  for every good bought'));
push(B('Marginal utility is the same idea as marginal benefit. If marginal benefit per dollar is higher on one good, spending shifts toward it.'));
push(S('§5.3  From the Buyer’s Problem to the Demand Curve'));
push(B('The demand curve is traced by solving the buyer’s problem at each price and recording the optimal quantity. A price change pivots the budget constraint and moves the optimal bundle.'));
push(B('Market demand is the horizontal sum across buyers.'));
push(S('§5.4  Consumer Surplus'));
push(D('Consumer surplus','willingness to pay minus price paid, summed over the units bought; the area below the demand curve and above the market price.'));
push(FM('CS on a straight-line demand  =  ½ × base × height','base  =  quantity','height  =  demand intercept − market price'));
push(B('Because marginal benefit diminishes, each additional unit adds less surplus than the one before.'));
push(S('§5.5  Demand Elasticities'));
push(D('Price elasticity of demand','the responsiveness of quantity demanded to a change in price.'));
push(FM('E  =  %ΔQ / %ΔP','Midpoint method: each change divided by the average of the old and new values'));
push(L('|E| > 1  elastic'));
push(L('|E| < 1  inelastic'));
push(L('|E| = 1  unit elastic'));
push(L('vertical curve  perfectly inelastic'));
push(L('horizontal curve  perfectly elastic'));
push(B('Total revenue: elastic demand, a price cut raises revenue; inelastic demand, a price rise raises revenue; unit elastic, total spending is unchanged.'));
push(B('Demand is more elastic with more substitutes, a larger share of the budget, and more time to adjust.'));
push(FM('Cross-price elasticity  =  %ΔQ of A / %ΔP of B'));
push(L('positive → substitutes'));
push(L('negative → complements'));
push(L('zero → unrelated'));
push(FM('Income elasticity  =  %ΔQ / %Δincome'));
push(L('negative → inferior good'));
push(L('between 0 and 1 → normal necessity'));
push(L('above 1 → normal luxury'));
push(GT([
 'Budget constraint before and after a change: slope, position, or both.',
 'Demand curve with a price line: consumer surplus as an area, and its change when price moves.',
 'Total-benefit table across goods: the affordable bundle with the highest total benefit.',
 'Elasticity table: the elasticity multiplied by the percentage change, and the sign.']));

push(H('Chapter 6 — Sellers and Incentives'));
push(S('§6.1  Sellers in a Perfectly Competitive Market'));
push(B('Conditions: sellers produce identical goods; no buyer or seller is large enough to influence the market price; there is free entry and exit.'));
push(D('Free entry','entry unobstructed by legal or technical barriers.'));
push(D('Price taker','a seller too small to affect the market price.'));
push(B('An individual firm faces a horizontal demand curve at the market price. The industry faces a downward-sloping demand curve.'));
push(S('§6.2  The Seller’s Problem'));
push(B('The seller’s problem has three parts: production, costs, and revenues.'));
push(D('Production function','the relationship between inputs and the output they produce.'));
push(D('Marginal product','the additional output from one more unit of an input.'));
push(D('Specialization','the range over which marginal product is rising.'));
push(D('Diminishing returns','the range over which marginal product is falling but still positive.'));
push(B('Beyond that range marginal product is negative and total output falls.'));
push(D('Fixed cost','does not vary with output.'));
push(D('Variable cost','varies with output.'));
push(D('Sunk cost','a cost already committed that can never be recovered; irrelevant to current decisions. Fixed costs are sunk in the short run.'));
push(D('Explicit cost','a direct monetary payment.'));
push(D('Implicit cost','the opportunity cost of a resource already owned.'));
push(FM('Accounting profit  =  TR − explicit costs','Economic profit  =  TR − explicit costs − implicit costs'));
push(B('Economic profit is never larger than accounting profit. Zero economic profit means positive accounting profit.'));
push(FM('AFC  =  FC / Q','AVC  =  VC / Q','ATC  =  TC / Q  =  AFC + AVC','MC  =  ΔTC / ΔQ','Profit  =  (P − ATC) × Q'));
push(B('MC cuts AVC and ATC at their minimum points, from below. Fixed cost is the gap between ATC and AVC multiplied by quantity.'));
push(D('Efficient scale','the quantity at which average total cost is at its minimum; there MC = ATC.'));
push(D('Economies of scale','LRATC falls as output rises.'));
push(D('Constant returns to scale','LRATC is flat.'));
push(D('Diseconomies of scale','LRATC rises.'));
push(B('Specialization is one source of economies of scale.'));
push(S('§6.3  From the Seller’s Problem to the Supply Curve'));
push(FM('Profit-maximizing output:  P  =  MC','Firm’s short-run supply: MC at every price at or above minimum AVC'));
push(D('Price elasticity of supply','%ΔQ supplied / %ΔP; positive, because a higher price raises quantity supplied.'));
push(B('A supply curve is unit-elastic when it is a straight line through the origin, whatever its slope. Supply is more elastic with more time to adjust and more spare capacity.'));
push(S('§6.4  Producer Surplus'));
push(D('Producer surplus','price received minus willingness to accept, summed over the units sold; the area above the supply curve and below the market price.'));
push(W('Producer surplus and profit','producer surplus subtracts variable costs only; profit also subtracts fixed costs.'));
push(FM('PS on a straight-line supply  =  ½ × base × height','base  =  quantity sold','height  =  price − supply intercept'));
push(S('§6.5  From the Short Run to the Long Run'));
push(B('Short run: at least one input is fixed, and fixed costs are paid whether or not the firm produces. Long run: every input is adjustable and the firm may leave the industry.'));
push(FM('Shut down, short run, if  P < minimum AVC','Exit, long run, if  P < minimum ATC'));
push(B('A firm that shuts down still pays its fixed cost. A firm that exits does not.'));
push(S('§6.6  Long-Run Competitive Equilibrium'));
push(B('Economic profits attract entry, shifting market supply right and lowering the price. Losses cause exit, shifting market supply left and raising the price.'));
push(FM('Long-run equilibrium:  P  =  minimum ATC','Economic profit  =  0'));
push(GT([
 'Cost-curve diagram with MC, AVC, ATC and MR: profit-maximizing quantity, shutdown point, break-even point, and fixed cost, profit or loss as an area.',
 'Total-output table: marginal product, and the boundaries between specialization, diminishing returns, and negative returns.',
 'Supply schedules for individual firms: horizontal summation, and willingness to accept for a given unit.',
 'Supply curve with a price line: producer surplus as an area, and its change when price moves.',
 'Industry diagram with entry or exit: which curve moves, which way, and where the process stops.',
 'LRATC curve: economies of scale, constant returns to scale, diseconomies of scale.']));

/* ═══════ PART TWO ═══════ */
push(PART('Part Two  ·  Chapters 7, 8, 9, 10, 12'));

push(H('Chapter 7 — Perfect Competition and the Invisible Hand'));
push(S('§7.1  Perfect Competition and Efficiency'));
push(D('Social surplus (total surplus)','consumer surplus plus producer surplus.'));
push(B('At the competitive equilibrium every unit worth at least its cost is traded, and no unit is traded whose cost exceeds its value. Social surplus is therefore at its maximum.'));
push(W('Departures in both directions','below the equilibrium quantity, valuable trades go unmade; above it, units are produced that cost more than they are worth. Social surplus falls either way.'));
push(D('Pareto efficient','an allocation in which nobody can be made better off without making somebody else worse off.'));
push(W('Pareto efficiency and surplus maximization','two distinct properties. Pareto efficiency concerns whether anyone can gain without harm to another; surplus maximization concerns the size of the total. A competitive equilibrium has both.'));
push(D('Deadweight loss','the social surplus that a market intervention destroys. Not transferred to anyone.'));
push(B('Trades that do not occur at the equilibrium price represent no lost surplus: the non-buyer values the unit below the price, and the non-seller’s cost lies above it.'));
push(B('Given lists of willingness to pay and willingness to accept, a trade occurs wherever value ≥ cost. Consumer surplus is the sum of (WTP − price) over the units traded; producer surplus is the sum of (price − WTA).'));
push(FM('CS  =  ½ × Q × (demand intercept − P)','PS  =  ½ × Q × (P − supply intercept)'));
push(GT([
 'Reservation-value tables: who trades, and the surplus on each side.',
 'Linear demand and supply: consumer surplus and producer surplus as areas.',
 'A restriction cutting quantity below equilibrium: the deadweight loss as an area.']));

push(S('§7.3  Allocation of Resources Across Industries'));
push(B('Profits and losses move resources between industries: positive economic profit draws resources in, losses drive them out.'));
push(FM('Long-run competitive equilibrium:  P  =  MC  =  minimum ATC','Economic profit  =  0'));
push(B('Entry shifts market supply right and the price falls; exit shifts it left and the price rises. The process ends at zero economic profit.'));
push(W('Short run and long run after a shock','in the short run the number of firms is fixed and each firm alters its own output. In the long run firms enter or leave, the price returns to minimum ATC, and each surviving firm returns to efficient scale; the permanent change is in the number of firms.'));
push(B('Where two goods use similar resources and one becomes more profitable, producers switch to it: its price falls, the other’s rises, and profitability is equalized.'));
push(GT([
 'Firm cost curves with a price line: profit or loss, and therefore entry or exit.',
 'Market diagram with two supply curves: which way supply moved, and the old and new price.']));

push(S('§7.4  Prices Guide the Invisible Hand'));
push(B('A price performs three functions: it signals scarcity, it gives sellers an incentive to supply more, and it rations the existing quantity to the buyers who value it most.'));
push(B('A central planner setting quantity targets has none of that information and provides no reward for obtaining it. Free prices are the mechanism by which a market allocates resources without central direction.'));
push(B('A rising price draws supply toward the shortage and allocates existing stock to the buyers who value it most.'));
push(B('A binding ceiling suspends that mechanism: a shortage appears and allocation passes to queues, waiting lists or chance.'));
push(W('The two parts of a price control','part of the sellers’ loss is a transfer: the buyers who still buy pay less, and that surplus is still held by someone. The remainder is deadweight loss, on the trades that no longer occur, held by no one.'));
push(GT([
 'A ceiling or floor with lettered areas: which area is the transfer, which is the deadweight loss.',
 'Reservation-value tables at a controlled price: units still traded, and the surplus on each side.']));

push(S('§7.5  Equity and Efficiency'));
push(B('Efficiency concerns the size of the total. Equity concerns its division. The two criteria can rank outcomes differently.'));
push(W('Efficiency and fairness','distinct criteria. The size of the total and the trade-off between the two can be measured; how the total should be divided cannot be settled by that measurement.'));
push(B('Redistribution can improve equity at a cost in efficiency, since taxes and transfers alter incentives to work, save and bear risk. Complete equalization removes the reward for effort entirely.'));
push(B('Of two outcomes, the one with the larger total surplus is the more efficient. Which is preferable overall is a separate, normative question.'));

push(H('Chapter 8 — Trade'));
push(S('§8.1  The Production Possibilities Curve'));
push(D('Production possibilities curve','the maximum of one good for a given level of the other. Also called the production possibilities frontier.'));
push(B('Points on the curve are efficient; points inside are attainable but inefficient; points beyond are unattainable.'));
push(D('Straight-line PPC','constant opportunity cost.'));
push(D('Bowed-out PPC','combination of multiple PPCs, with increasing opportunity cost — each additional unit of one good costs more of the other as we move from the most productive to the least.'));
push(FM('Straight-line PPC: opportunity cost of one X  =  (maximum Y) / (maximum X)','The two opportunity costs are reciprocals'));
push(GT([
 'A PPC with points inside, on and beyond it: attainable, efficient, impossible.',
 'A straight-line PPC: the opportunity cost of each good, in both directions. Refer to lecture slides.',
 'A constraint in hours, days or workers: the maximum of each good, and the time a stated combination takes.']));

push(S('§8.2  The Basis for Trade: Comparative Advantage'));
push(D('Absolute advantage','the ability to produce more output than another agent with the same resources.'));
push(D('Comparative advantage','the ability of one economic agent to produce at a lower opportunity cost than another.'));
push(W('Absolute and comparative advantage','a producer may hold an absolute advantage in both goods and a comparative advantage in only one. Comparative advantage concerns what is given up; absolute advantage concerns output from given resources.'));
push(B('In an output table, the opportunity cost of one good is the other good’s output divided by its own. Each party specializes where its own opportunity cost is lower.'));
push(D('Terms of trade','the price of one good in terms of the other; the exchange rate between goods.'));
push(W('Range of acceptable terms','the terms of trade lie between the two parties’ opportunity costs. A rate outside that range leaves one party worse off than self-production, and no trade occurs.'));
push(B('With specialization and trade a party consumes beyond its own production possibilities curve. This is the gain from trade.'));
push(GT([
 'Output tables: opportunity costs for both parties, and each kind of advantage.',
 'A stated exchange rate: whether it lies between the two opportunity costs.',
 'A PPC with a consumption point outside it: how trade makes that point reachable.']));

push(S('§8.3  Trade Between States'));
push(B('The same logic applies within a country: regions with different opportunity costs specialize and trade, and both consume more than in isolation.'));
push(B('Additional resources or improved technology shift a PPC outward. An improvement affecting one good only pivots it.'));
push(B('A region exports the good of its comparative advantage and imports the other.'));

push(S('§8.4  Trade Between Countries'));
push(D('World price','where world supply of a good meets world demand.'));
push(B('A world price below the no-trade domestic price makes the country an importer; a world price above it makes the country an exporter.'));
push(FM('Imports  =  quantity demanded at the world price  −  quantity supplied at the world price'));
push(B('On opening to trade as an importer, consumers gain and domestic producers lose; the gain exceeds the loss and total surplus rises. As an exporter the roles reverse and total surplus rises again.'));
push(W('Gains from trade are a statement about totals','within each country some parties lose. The winners gain more than the losers lose, so full compensation is possible in principle.'));
push(B('Differences in resources, capital and technology are what make one country’s costs differ from another’s.'));
push(GT([
 'A domestic market with a world price line: imports or exports as the horizontal gap.',
 'The same market before and after opening to trade: who gains, who loses, and total surplus.']));

push(S('§8.5  Arguments Against Free Trade'));
push(B('The standard arguments are national security; protection of an infant industry; cultural identities; countering unfair competition such as dumping or subsidized production; and protection of domestic jobs and wages.'));
push(D('Tariff','a tax added to the price of an imported product.'));
push(B('A tariff divides the consumer loss into four parts:'));
push(Lb('Extra producer surplus','to domestic firms.'));
push(Lb('Government revenue','the tariff multiplied by the quantity still imported.'));
push(Lb('Two deadweight-loss triangles','domestic production costing more than the world price, and consumption that no longer happens.'));
push(W('Transfer and loss','the producer gain and the tariff revenue are transfers, still held by someone. The two triangles are destroyed. Foreign exporters also lose producer surplus, but that is not counted in domestic social surplus.'));
push(GT([
 'A tariff diagram with lettered areas: who receives each, and which are lost to everyone.',
 'The same diagram: total consumer loss and how it divides.']));

push(H('Chapter 9 — Externalities and Public Goods'));
push(S('§9.1  Externalities'));
push(D('Externality','an economic activity has either a spillover cost to, or a spillover benefit for, a bystander — somebody who is not party to the transaction.'));
push(D('Marginal social cost','private marginal cost plus marginal external cost.'));
push(W('Third parties only','the test is not whether somebody was made worse off by the price. It is whether they were a party to the transaction.'));
push(D('Pecuniary externality','when a market exchange affects other people through market prices. It is a transfer through prices — not a market failure, and it creates no deadweight loss.'));
push(B('Under a negative externality the market overproduces, the external cost being ignored. Under a positive externality it underproduces, the external benefit being ignored.'));
push(B('A competitive market with no externalities maximizes total surplus at its equilibrium. With externalities it does not, and is therefore a market failure.'));
push(FM('Social optimum: the quantity where demand meets marginal social cost'));
push(W('The price at the social optimum','at the socially optimal quantity the price is the height of the demand curve, not of a cost curve.'));
push(B('The deadweight loss of an uncorrected negative externality is the triangle between marginal social cost and demand, over the units between the optimal and the market quantity.'));
push(GT([
 'Private supply with marginal social cost: market quantity, socially optimal quantity, and the optimal price read off demand.',
 'The same diagram: the deadweight loss as an area.']));

push(S('§9.2  Private Solutions to Externalities'));
push(D('Coase theorem','with clear property rights and low transaction costs, private bargaining reaches an efficient allocation, whoever holds the right.'));
push(W('Assignment of the right','the efficient activity level is the same whichever party holds the right; only the direction of payment differs.'));
push(B('The efficient outcome continues the activity when its benefit exceeds the harm, and ends it when the harm exceeds the benefit.'));
push(B('Private bargaining fails when transaction costs are high or when too many parties are affected.'));

push(S('§9.3  Government Solutions to Externalities'));
push(D('Pigouvian tax','a per-unit tax equal to the marginal external cost, which lifts private supply onto marginal social cost.'));
push(FM('Corrective tax per unit  =  vertical gap between marginal social cost and private supply'));
push(D('Quantity limit (quota)','a cap on quantity. Set at the socially optimal quantity it reaches the same outcome by another route.'));
push(W('Tax and quota on the diagram','the corrective tax is a vertical distance between the two cost curves. The price under a binding cap is the height of the demand curve at the permitted quantity.'));
push(D('Command-and-control regulation','the government sets the amount of an activity rather than its price.'));
push(GT([
 'Private supply with marginal social cost: the corrective tax as a vertical gap at the optimum.',
 'The same diagram with a quantity cap: the price read off demand at the capped quantity.',
 'The deadweight loss of the uncorrected externality as an area.']));

push(S('§9.4  Public Goods'));
push(D('Excludable','non-payers can be prevented from consuming it.'));
push(D('Rival','one person’s consumption reduces what is left for others.'));
push(Lb('Private good','excludable and rival.'));
push(Lb('Club good','excludable, non-rival.'));
push(Lb('Common pool resource','non-excludable, rival.'));
push(Lb('Public good','non-excludable and non-rival.'));
push(D('Free-rider problem','an individual does not pay for a good because it is nonexcludable, and consumes it anyway. This is why voluntary funding under-provides public goods and why taxation is used instead.'));
push(W('Horizontal and vertical summation','for a private good, quantities are added at a given price. For a public good, willingness to pay is added at a given quantity, since all consumers consume the same units simultaneously.'));
push(FM('Public good optimum: vertically summed willingness to pay  =  marginal cost'));
push(B('The same rule determines the provision of a shared amenity within a small group: the sum of the members’ marginal benefits against marginal cost.'));
push(B('Excluding non-payers from a public good removes the non-excludability that defines it.'));
push(GT([
 'Two individual demand curves with a marginal cost curve: which summation is right for a public good, and the optimal quantity.',
 'A good described in words: its position in the rivalry-and-excludability grid.']));

push(S('§9.5  Common Pool Resource Goods'));
push(D('Common pool resource','non-excludable but rival.'));
push(D('Tragedy of the commons','open access plus depletion through use. A negative externality with no owner to bargain with.'));
push(W('Common pool resources and public goods','both are non-excludable; they differ in rivalry. Rivalry is the source of depletion, so a non-rival good cannot be over-used.'));
push(B('Remedies are the same three as for any externality: assign property rights, tax or cap use, or regulate access.'));

push(H('Chapter 10 — Taxation, Regulation and Government Failure'));
push(S('§10.1.3  Tax Incidence and Deadweight Loss'));
push(D('Tax incidence','who actually bears the burden of a tax, measured by whose income falls, not by whose name is on the payment.'));
push(D('Statutory incidence','who the law makes liable for the tax.'));
push(D('Economic incidence','whose income falls.'));
push(W('Statutory side is irrelevant to the outcome','a per-unit tax on sellers shifts supply up by the tax; the same tax on buyers shifts demand down by the tax. Both yield the same quantity, the same buyers’ price, the same sellers’ price and the same division of the burden.'));
push(FM('Buyers’ price  −  sellers’ price  =  the tax, the wedge'));
push(FM('Tax revenue  =  tax per unit  ×  post-tax quantity'));
push(FM('Deadweight loss  =  ½  ×  tax per unit  ×  fall in quantity'));
push(B('The wedge divides into three areas: the buyers’ share, the sellers’ share, and the deadweight-loss triangle. Tax revenue is the first two combined.'));
push(W('Incidence and elasticity','the burden falls on the less elastic side. A perfectly elastic side bears none of the tax; a perfectly inelastic side bears all of it.'));
push(B('With perfectly elastic supply the buyers’ price rises by the full tax. With perfectly elastic demand the buyers’ price does not rise and sellers bear the full tax.'));
push(GT([
 'A market before and after a per-unit tax: buyers’ price, sellers’ price, quantity, revenue, deadweight loss.',
 'The same tax on the other side: which curve moves, and that the outcome is identical.',
 'A wedge with lettered areas: buyers’ share, sellers’ share, deadweight loss, and which areas form revenue.',
 'Curves of different elasticities: which side bears more.']));

push(S('§10.2  Regulation'));
push(B('A binding ceiling produces a shortage; a binding floor produces a surplus. Both reduce the quantity traded and create deadweight loss.'));
push(B('From schedules at a controlled price: consumer and producer surplus are summed over the units that still trade; the surplus on the units no longer traded is the deadweight loss.'));
push(W('A control only bites from one side','a ceiling acts only below the market price and a floor only above it. The regulation need not change for its effect to disappear: if the market moves under a fixed ceiling until it would clear below it, there is no shortage and no deadweight loss at all.'));
push(B('A tax changes the price and lets the market pick the quantity. Direct regulation picks the quantity. A price control picks the price and lets neither side clear.'));
push(GT([
 'Schedules with a ceiling or floor: units traded, consumer surplus, producer surplus, deadweight loss.',
 'Rent control over time: which curve moves in the long run.']));

push(S('§10.3  Government Failures'));
push(D('Government failure','inefficiency caused by the government’s own intervention.'));
push(Lb('Cost of bureaucracy','staffing an agency uses real resources. The true cost is what those people would have produced elsewhere, not their salaries.'));
push(Lb('Corruption','resources spent obtaining or granting favourable treatment produce nothing.'));
push(Lb('Underground economy','a tax or rule can move activity out of the recorded market rather than stopping it, so revenue rises by less than expected and the recorded fall overstates the real one.'));

push(H('Chapter 12 — Monopoly'));
push(S('§12.1  Introducing a New Market Structure'));
push(D('Monopoly','one seller of a good or service with no close substitutes.'));
push(D('Market power','the ability to set the price.'));
push(B('A monopolist is a price maker and faces the entire market demand curve, selecting a point on that curve rather than accepting a given price.'));

push(S('§12.2  Sources of Market Power'));
push(D('Barriers to entry','circumstances that prevent potential competitors from entering the market.'));
push(Lb('Legal barriers','patents, copyrights, licenses, exclusive franchises. A patent makes rival production unlawful, which is what holds price above marginal cost.'));
push(Lb('Control of a key resource','ownership of an input no rival can obtain.'));
push(Lb('Economies of scale','average total cost still falling over the range the market demands.'));
push(Lb('Network externalities','the product is worth more because others use it.'));
push(D('Natural monopoly','economies of scale over the whole market: average total cost is still falling when one firm has served everybody.'));
push(W('Cost-side and demand-side barriers','economies of scale act on the cost curve: one firm is cheaper. Network effects act on demand: buyers prefer the firm others already use.'));
push(GT([
 'Demand with constant marginal cost and falling average total cost: whether average total cost is still falling where demand meets it.']));

push(S('§12.3  The Monopolist’s Problem'));
push(B('A competitive firm sells any quantity at the market price, so its marginal revenue equals that price. A monopolist must lower the price to sell more, and the lower price applies to every unit sold.'));
push(D('Marginal revenue','the change in total revenue from one more unit. It is not the price.'));
push(FM('TR  =  P × Q','MR  =  ΔTR / ΔQ','For a monopolist,  MR < P'));
push(D('Quantity effect','more units are sold.'));
push(D('Price effect','every unit already being sold now earns less.'));
push(B('Marginal revenue is the sum of the two effects. The price effect grows with output, since the price cut applies to a larger number of existing units.'));
push(W('Slope of marginal revenue','on straight-line demand, marginal revenue shares the vertical intercept and falls at twice the rate. This follows from the price effect growing with output.'));
push(FM('Total revenue is at its maximum where  MR  =  0'));
push(W('Operating range','a monopolist does not operate where demand is inelastic. Marginal revenue is negative there, so a cut in output would raise revenue and lower cost at once.'));
push(B('Total revenue rises while the quantity effect dominates, peaks where the two effects cancel, and falls where the price effect dominates.'));
push(GT([
 'Demand with marginal revenue: the quantity where MR = 0, the price there, and maximum total revenue.',
 'A price and quantity pair before and after a change: which effect dominated.',
 'A price and quantity schedule: differencing total revenue for marginal revenue, and where it turns negative.']));

push(S('§12.4  Choosing the Optimal Quantity and Price'));
push(FM('Quantity where  MR  =  MC','Price read up on the demand curve at that quantity'));
push(W('Which curve sets which','marginal revenue locates the quantity; the demand curve sets the price.'));
push(FM('Profit  =  (P − ATC) × Q','ATC read at the profit-maximizing quantity'));
push(W('Height of the profit rectangle','price minus average total cost, not price minus marginal cost.'));
push(B('Revenue is largest where MR = 0; profit is largest where MR = MC. Marginal cost is positive, so the profit-maximizing quantity is the smaller of the two and its price the higher.'));
push(GT([
 'A monopolist’s demand, marginal revenue, marginal cost and average total cost: quantity, price, and profit as a rectangle.',
 'A price and quantity schedule with constant marginal cost: profit-maximizing output and profit.',
 'The revenue-maximizing price against the profit-maximizing price.']));

push(S('§12.5  The Cost of Monopoly'));
push(B('Relative to a competitive market with identical demand and costs, a monopolist produces less and charges more:'));
push(Lb('Consumer surplus','falls.'));
push(Lb('Producer surplus','rises.'));
push(Lb('Deadweight loss','positive, where competition had none.'));
push(Lb('Social surplus','falls, by exactly the deadweight loss.'));
push(W('Transfer and deadweight loss','the rectangle between the two prices, over the units still sold, is a transfer held by the monopolist. The triangle over the units no longer sold is deadweight loss, held by no one.'));
push(B('A transfer changes who holds the surplus; deadweight loss destroys it. Deadweight loss is the social cost of monopoly, as distinct from its distributional effect.'));
push(GT([
 'One market under monopoly and under competition: the two quantities and prices, consumer surplus, the transfer, and the deadweight loss as separate areas.']));

/* ═══════ KEY FORMULAS ═══════ */
push(PART('Key Formulas'));
push(S('Choice and the margin'));
[ 'Net benefit = total benefit − total cost',
  'Expand while MB ≥ MC; optimum where MB = MC',
  'Opportunity cost of time = hours × value per hour',
  'Budget constraint: P₁Q₁ + P₂Q₂ = income; slope = − P₁/P₂',
  'Equal-marginal principle: MB₁/P₁ = MB₂/P₂ for every good bought'
].forEach(x=>push(L(x)));
push(S('Surplus and welfare'));
[ 'CS = willingness to pay − price paid',
  'PS = price − willingness to accept',
  'Social surplus = CS + PS, plus government revenue where a tax or tariff applies',
  'Deadweight loss = social surplus in the efficient outcome − social surplus now',
  'Triangle = ½ × base × height',
  'Rectangle = base × height',
  'Transfer = a rectangle somebody still holds',
  'Deadweight loss = a triangle nobody holds'
].forEach(x=>push(L(x)));
push(S('Elasticity'));
[ 'Price elasticity = %ΔQ / %ΔP, midpoint base = average of old and new',
  'Cross-price elasticity = %ΔQ_A / %ΔP_B',
  'Income elasticity = %ΔQ / %Δincome',
  'A tax burden falls on the less elastic side'
].forEach(x=>push(L(x)));
push(S('Costs, the firm and competition'));
[ 'Accounting profit = TR − explicit',
  'Economic profit = TR − explicit − implicit',
  'MC = ΔTC/ΔQ',
  'AVC = VC/Q',
  'ATC = TC/Q',
  'AFC = FC/Q',
  'Fixed cost = (ATC − AVC) × Q',
  'Marginal product = Δoutput / Δinput',
  'Profit = (P − ATC) × Q',
  'Competitive firm: P = MC',
  'Competitive firm’s supply: MC at prices at or above minimum AVC',
  'Shut down if P < min AVC',
  'Exit if P < min ATC',
  'Long-run competitive equilibrium: P = MC = min ATC, economic profit = 0'
].forEach(x=>push(L(x)));
push(S('Trade'));
[ 'Straight-line PPC: opportunity cost of one X = (maximum Y) / (maximum X)',
  'Comparative advantage: the lower opportunity cost',
  'Absolute advantage: the higher output',
  'Terms of trade lie between the two parties’ opportunity costs',
  'Imports = quantity demanded at the world price − quantity supplied at the world price',
  'Tariff revenue = tariff per unit × quantity still imported'
].forEach(x=>push(L(x)));
push(S('Externalities and public goods'));
[ 'Marginal social cost = private marginal cost + marginal external cost',
  'Social optimum: demand meets marginal social cost; price read off demand',
  'Pigouvian tax = marginal external cost',
  'Private good: sum demand horizontally',
  'Public good: sum demand vertically'
].forEach(x=>push(L(x)));
push(S('Taxes and monopoly'));
[ 'Buyers’ price − sellers’ price = the tax',
  'Tax revenue = tax per unit × post-tax quantity',
  'Deadweight loss of a tax = ½ × tax × fall in quantity',
  'TR = P × Q',
  'MR = ΔTR/ΔQ',
  'Monopolist: MR < P',
  'Total revenue largest where MR = 0',
  'Profit largest where MR = MC',
  'Monopoly price: find Q where MR = MC, then read P off demand',
  'Monopoly profit = (P − ATC) × Q, ATC read at that quantity'
].forEach(x=>push(L(x)));

const doc=new Document({
  numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,
    style:{paragraph:{indent:{left:400,hanging:200}}}}]}]},
  styles:{default:{document:{run:{font:F,size:22,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1150,bottom:1150,left:1150,right:1150}}},children:k}]});
const {writeVersioned}=require('./ver.js');
Packer.toBuffer(doc).then(b=>{const o=writeVersioned('ECON003_Final_Study_Guide',b);
  console.log('->',o.name,'|',b.length,'bytes |',k.length,'paragraphs');});
