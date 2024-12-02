**Quantifying and Mapping Predicted Package Demand for Last-Mile Drone
Delivery**

# Abstract {#abstract .list-paragraph}

# Introduction

The prospect of drone delivery is a frequent topic in the popular media.
As of October 2024, there have been some small-scale commercial
deployments in the U.S. For example, in July 2024, the FAA authorized
Zipline and Wing to fly commercial drones beyond visual line of sight
(Jones, 2024).

Drones are well-suited to last-mile delivery, which accounts for \~53%
of total worldwide shipping costs (Forbes, 2023), with labor costs
accounting for 90% of the delivery cost (Shetty et al., 2022). These
high costs are due to the difficulty of gathering and putting shipments
together and the dispersal of destinations (Macioszek et al., 2017).
Delivery drones are by definition uncrewed, and most are expected to
operate autonomously, removing the need for delivery drivers and
potentially reducing the need for extensive human intervention. Because
drones can carry smaller payloads cost-efficiently (Rahmani et al.,
2024), point-to-point routing is feasible, though smaller payloads also
mean more drones must be loaded, controlled, and coordinated.
Narkus-Kramer (2017) estimated that wide-scale implementation of drones
for last-mile delivery can decrease total delivery cost of \<5 lbs.
packages from \$5.00 per package to \$1.41−2.76 per package.

Last-mile delivery refers to the final leg of the supply chain, where
goods are transported from a transportation hub to the final delivery
destination. It is one of most polluting segments of the supply chain
(Brown et al., 2014). (Jaller et al., 2021) estimated that Total Cost of
Ownership (TCO) for conventional diesel medium-duty truck vehicles
ranges from \$282,000 to \$305,000, with the cost of negative public
health impacts due to emissions ranging from \$38,000 to \$64,000 over
the vehicle lifetime. Replacing fossil-fueled vehicles with electrically
powered drones can directly reduce emissions, along with the attendant
benefits of reduced road congestion.

Proponents of drone delivery claim that it offers rapid turnaround from
order placement to delivery. For example, in March 2024, DoorDash, in
partnership with Alphabet's Wing, announced the roll-out of their new
drone fast food delivery, with deliveries expected to "arrive between 10
to 30 minutes, carried by drones that travel at around 65 mph" (Davis,
2024). For context, the average global food delivery time with Uber Eats
is less than 30 minutes (Tarca, 2022), and DoorDash claims an average
time of \~40 minutes (DoorDash, 2024). Modern shoppers have come to
expect their purchases within one or two days of placing an order, with
the maximum delivery time that shoppers are willing to accept for free
shipping decreasing from 5.5 days in 2012 to 3.5 days in 2024 (Alix and
Partners, 2024). In the United States in 2023, approximately 167 million
people paid for Amazon Prime membership and the convenience of two-day,
and in some urban areas, one- or same-day shipping (Howarth, 2023).
Consumers are more inclined to purchase products with shorter shipping
times, for example, Fisher et al. (2019) estimated that U.S. apparel
online store sales increased by 1.45% per business day reduction in
delivery time.

But most people have yet to see drones delivering packages in their
neighborhoods. Several intertwined factors make achieving drone
deliveries at large scale difficult, including safety, noise, and
privacy concerns, the need for regulatory approval, and the technical
challenges of incorporating drones into existing air traffic control
systems (Yoo et al., 2018; Dorling et al., 2017). It is also not clear
how much demand there is for drone delivery, whether consumers will be
willing to pay a premium for drone delivery, or somewhat conversely,
whether operators and regulators can support, and communities will
accept, high levels of drone traffic, especially in urban areas.

Here, we consider the demand aspect. Accurate demand predictions that
reflect the factors driving consumer demand and determine how that
demand varies by location and over time are essential for the
development of airspace management strategies and for planning the
necessary infrastructure to support these operations, including charging
stations, vertiports, and maintenance facilities. Operators also need
reliable demand estimations to guide investment decisions and facilitate
the development of profitable business models.

While a few researchers have proposed demand models (#add references),
most of these models have limited applicability across diverse
scenarios. Many existing models are location-specific, focusing on
particular urban areas or unique study cases (#add references). Which
hinders their generalizability to different geographic locations.
Additionally, temporal dynamics and consumer behavior factors are
frequently underexplored, further restricting the flexibility of these
models in adapting to different study locations. Consequently, there is
a need for more generalized frameworks capable of accommodating diverse
spatial and demographic contexts, ensuring broader applicability.

To address this gap, this paper develops a generalizable, spatially
explicit model for estimating consumer demand for last-mile drone
delivery across the United States. In Section 2, we identify the key
market demand drivers for last-mile drone delivery services. Census
data. In Section 3, we develop a spatially explicit, high-resolution,
generalizable model to estimate consumer demand for last-mile drone
delivery across the United States, accounting for variations across
space and time. The model uses publicly available data sources --
OpenStreetMap and U.S. Census data. By integrating the data into
statistical frameworks, we aim to quantify, and map predicted package
demand at a high spatial resolution, providing insights adaptable to
different geographic locations and time periods. We demonstrate our
model on case studies of Austin, TX and West Lafayette, IN in Section 4.
Section 5 discusses the implications of the findings. Finally, Section 6
concludes the paper by summarizing the insights, limitations and
suggesting future research directions.

# Drone Last-Mile Delivery Modelling

**\*\*\*I think this discussion should come first, and then we can
figure out what to do with the demand drivers stuff\*\*\***

This section reviews current models used for estimating drone delivery
demand, their underlying methodologies, and their limitations. We
identified four main modeling approaches, as discussed next.

## Historical Data-Based Predictive Scaling Models 

Existing data from traditional package delivery services can serve as a
basis for projecting future drone delivery demand. Researchers
extrapolate from existing trends and scale the data based on assumptions
about the proportion of deliveries suitable for drones. For example,
Oosedo (2021) used a predictive scaling model to estimate future parcel
delivery demand in Japan using historical parcel delivery data,
population data, and growth rates. The model scales parcel deliveries
proportionally to population growth, and then applies growth rates to
project future demand. This approach is effective for initial estimates
of demand in areas where historical delivery data is available.

Similarly, Narkus-Kramer (2017) developed a predictive and economic
impact model for small autonomous UAS package delivery. They used
current package delivery volumes and projected future growth scenarios
to estimate the potential benefits of drone delivery in densely
populated urban environments like the Washington, D.C. metropolitan
area. They also quantified the economic impacts of drone delivery, in
dollar equivalent \*\*\*and so?\*\*\*.

Doole (2020) used a traffic density estimation model to assess urban
airspace capacity and demand for drone deliveries in very low-level
urban airspace across European cities. By using population and
historical demand data, Doole et al. (2020) estimated traffic density
for drone deliveries, revealing that high traffic density areas such as
Paris could support extensive drone delivery operations, with a
projected traffic density of over 87,000 drones in operation at any
given time. While traffic density models like this one provide valuable
insights into airspace management, they do not account for individual
building-level demand or differentiate between types of deliveries.

These models all rely heavily historical data, which may not always be
available for all locations. Additionally, current predictive scaling
models lack the granularity required for drone delivery demand, which is
inherently spatial and requires a more detailed understanding of local
population.

## Subject Matter Expert Input:

Ayyalasomayajula et al. (2020) used a socio-economic analysis model to
estimate traffic demand for nineteen potential civilian and commercial
UAS applications across the United States. The Transportation System
Analysis Model (TSAM) was used in conjunction with expert input to
assess socio-economic factors, including population demographics,
location, and cost of alternative delivery modes such as trucks,
couriers, and rail. This mixed approach offers a comprehensive
understanding of how socio-economic factors influence UAS demand.

However, the model\'s reliance on expert input may introduce bias, and
the generalizability of the findings could be limited in different
geographical or economic contexts.

### Market Surveys and Questionnaires

Gomes et al. (2016) used surveys to obtain data on preferred
transportation method across households in São Carlos, Brazil. They then
used a Kriging geostatistical method to estimate demand by spatially
interpolating travel mode choices across unsampled regions. The approach
involved using ordinary Kriging and indicator Kriging to predict the
number of households likely to opt for a particular mode of transport,
which can be adapted for predicting delivery demand.

In the context of drone delivery, a similar approach would involve
conducting surveys to gather information on consumer preferences,
willingness to opt for and pay for drone-based delivery services. By
analyzing obtained customer survey data alongside other available
variables, researchers can estimate delivery demand in areas with
limited direct data, enhancing the accuracy and coverage of demand
models.

This approach involves conducting market surveys and analyzing customer
data to understand preferences, willingness to adopt drone delivery, and
potential demand for different types of drone delivery services.

### Socio-economic Analysis

Data-driven models use socio-economic data to predict drone delivery
demand, assuming a correlation between factors like population density,
income level, housing type, and retail density with the demand for
package deliveries.

German et al. (2018) used population and income level metrics to predict
drone delivery demand for cargo deliveries using electric vertical
takeoff and landing (eVTOL) aircraft. Their model uses a demand
surrogate based on population and income levels, discretized by census
tracts. In their study of eVTOL operations in the San Francisco Bay
Area, they assume that areas with larger populations and higher average
incomes represent higher potential demand, under the assumption that
customers in such areas are more likely to pay for premium services like
faster delivery. The population was multiplied by average income to
obtain a total income metric per census tract, which was then used to
create a relative demand index for the placement of vertiports for cargo
delivery.

Gunady et al. (2022) similarly used a combination of population density,
income levels, housing type, and other demographics to estimate daily
package demand for middle-mile delivery using eVTOL vehicles in Chicago.
These metrics were aggregated at the census tract level, indicating a
fine-grained geographical analysis of the potential daily demand for
packages delivered by drones. The demographic information served as an
indicator of purchasing power and the probability of ordering packages
for delivery.

Similarly, Maheshwari et al. (2020) analyzed operational limits for air
taxi missions in Chicago, considering factors like vertiport locations,
ground traffic, and ridesharing. These models demonstrate the importance
of understanding spatial dynamics and how they can be leveraged to
efficiently allocate infrastructure resources.

Our method uses socio-economic analysis as the basis for demand
modeling.

### Current Limitations and Gaps in the Literature

While existing models provide valuable insights into demand estimation
for drone delivery, there are notable limitations that restrict their
broader applicability. Many models rely on proprietary datasets that are
not publicly available, limiting both reproducibility and application to
new locations. Additionally, most models lack sufficient spatial
resolution, making it difficult to capture neighborhood-level or
building-level demand variations that are crucial for last-mile delivery
planning.

Furthermore, many of the existing approaches assume homogeneity in
consumer preferences across different geographic regions, which can lead
to inaccuracies in demand estimation. For example, a model calibrated
for a densely populated metropolitan area may not be directly applicable
to a smaller suburban town due to differences in population density,
infrastructure, and socio-economic factors. In metropolitan areas, high
population density and diverse land use patterns can drive significant
demand for rapid, high-frequency delivery services, whereas suburban
towns may exhibit lower demand with different peak times and delivery
requirements.

None of the current models that we identified account for differences of
each building, which also leads to assuming homogeneity of demand across
the urban landscape.

In our model, we propose the use of OSM tags to classify buildings. We
also explore other options in Section 3.6.

The integration of temporal variables---such as peak delivery times and
seasonal variations---has also been limited in most existing studies.
Understanding temporal patterns is essential for optimizing delivery
schedules and ensuring efficient resource allocation. Our study aims to
address these limitations by developing a spatially explicit,
generalizable model that incorporates both spatial and temporal
dimensions of demand.

In summary, while existing literature provides useful frameworks and
insights, there is a lack of a generalizable, high-resolution spatial
demand model for drone delivery that can be applied across the United
States.

### Overview of existing methods drone delivery demand estimation.

Here\'s a comparison table summarizing demand and traffic density
estimations from the sources we've identified in the literature.

+------------+--------------+---------------+--------------+---------+
|   -        |              |   --          | **L          |         |
| ---------- | ------------ | ------------- | imitations** | ------- |
|            |   **Approach |   **Data and  |              | ------- |
|  **Study** |              |               |              |   **Loc |
|   -        | and Method** | Assumptions** |              | ation** |
| ---------- |              |   --          |              |         |
|            | ------------ | ------------- |              | ------- |
|   -        |              |               |              | ------- |
| ---------- |              |   --          |              |         |
|            | ------------ | ------------- |              |         |
|   -------  |              |               |              | ------- |
|            |   ---------  |   ----------  |              | ------- |
|   -------  |              |               |              |         |
|            |   ---------  |   ----------  |              |   ----  |
|            |              |               |              |         |
|            |              |               |              |   ----  |
+============+==============+===============+==============+=========+
|   -------- |              |               |   ---        |   --    |
|   Oosedo   | ------------ |  ------------ | ------------ | ------- |
|   (2021)   |   Predicts   |   Uses parcel |              |         |
|   -------- |   future     |   delivery    | Assumes that | Sendai, |
|            |   parcel     |   data and    |              |   Japan |
|   -------- |   delivery   |   population  |  past growth |   --    |
|            |   demand by  |   data,       |              | ------- |
|   -------  |   scaling    |   assuming    |  trends will |         |
|            |   historical |   that parcel |   continue   |   --    |
|   -------  |   data using |   deliveries  |   un         | ------- |
|            |   growth     |               | changed into |         |
|            |              |  will grow at |              |   ----  |
|            |  rates. This |               |  the future, |         |
|            |              |  a consistent |   w          |   ----  |
|            | simple model |   rate over   | hich may not |         |
|            |   projects   |   time.       |              |         |
|            |              |               |  account for |         |
|            | demand based |  ------------ |   market     |         |
|            |   on past    |               |   f          |         |
|            |   trends.    |               | luctuations. |         |
|            |              |  ------------ |   ---        |         |
|            | ------------ |               | ------------ |         |
|            |              |   ----------  |              |         |
|            |              |               |   ---        |         |
|            | ------------ |   ----------  | ------------ |         |
|            |              |               |              |         |
|            |   ---------  |               |   ---------  |         |
|            |              |               |              |         |
|            |   ---------  |               |   ---------  |         |
+------------+--------------+---------------+--------------+---------+
|   -----    |              |               |              |         |
| ---------- |  ----------- | ------------- | ------------ |  ------ |
|   Nar      |   Assesses   |   Relies on   |   Depends on | ------- |
| kus-Kramer |   the        |               |   the        |   Wash  |
|   (2017)   |   economic   |  package data |   assumption | ington, |
|   -----    |              |   from        |   that       |   D.    |
| ---------- |  and traffic |               |   e-commerce | C., USA |
|            |   impact of  | UPS/FedEx and |              |         |
|   -----    |   small      |   population  |  growth will |  ------ |
| ---------- |   drones     |   data,       |   persist at | ------- |
|            |   (UAS) for  |   assuming    |   current    |         |
|   -------  |   delivery   |   continued   |              |         |
|            |   using an   |   growth in   | rates, which |  ------ |
|   -------  |   economic   |   e-commerce  |              | ------- |
|            |   impact     |   activities. | may not hold |         |
|            |   model.     |               |              |   ----  |
|            |   Projects   | ------------- |  true in the |         |
|            |   future     |               |   long term. |   ----  |
|            |   scenarios  |               |              |         |
|            |   based on   | ------------- | ------------ |         |
|            |   current    |               |              |         |
|            |   data.      |   ----------  |              |         |
|            |              |               | ------------ |         |
|            |  ----------- |   ----------  |              |         |
|            |              |               |   ---------  |         |
|            |              |               |              |         |
|            |  ----------- |               |   ---------  |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |              |               |   --         |   -     |
|   Doole    | ------------ |  ------------ | ------------ | ------- |
|   (2020)   |   Estimates  |   Utilizes    |   M          |         |
|   -------- |   urban      |   population  | ay not fully |  Paris, |
|            |   airspace   |   data and    |              |         |
|   -------- |   traffic    |   delivery    |  account for |  France |
|            |              |   data to     |   the        |   -     |
|   -------  |  density for |   estimate    |              | ------- |
|            |   drone      |   traffic,    | complexities |         |
|   -------  |   delivery   |   assuming    |   and        |   -     |
|            |   using a    |   efficient   |              | ------- |
|            |   traffic    |   urban       |  regulations |         |
|            |   density    |   airspace    |              |   ----  |
|            |   estimation |   management  |  involved in |         |
|            |   model.     |   practices.  |   ma         |   ----  |
|            |   Focuses on |               | naging urban |         |
|            |   predicting |  ------------ |   a          |         |
|            |              |               | irspace with |         |
|            |  how crowded |               |   increased  |         |
|            |              |  ------------ |              |         |
|            | the airspace |               | drone usage. |         |
|            |              |   ----------  |   --         |         |
|            | will be with |               | ------------ |         |
|            |   drones.    |   ----------  |              |         |
|            |              |               |   --         |         |
|            | ------------ |               | ------------ |         |
|            |              |               |              |         |
|            |              |               |   ---------  |         |
|            | ------------ |               |              |         |
|            |              |               |   ---------  |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |   --         |               |   ----       |   ----  |
|   German   | ------------ |  ------------ | ------------ | ------- |
|   et al.   |   O          |   Uses        |   Economic   |   San   |
|   (2018)   | ptimizes the |   population  |   fea        |   Fr    |
|   -------- |              |   and income  | sibility and | ancisco |
|            | placement of |   data,       |   in         |   Ba    |
|   -------- |   vertiports |   aircraft    | frastructure | y Area, |
|            |              |   technical   |   lim        |   USA   |
|   -------  | (landing and |   details,    | itations may |   ----  |
|            |   ta         |   assuming    |   affect how | ------- |
|   -------  | ke-off spots |   limited     |   p          |         |
|            |              |   vertiport   | ractical and |   ----  |
|            |  for drones) |   locations   |              | ------- |
|            |              |               | accurate the |         |
|            | for electric |  and economic |              |   ----  |
|            |   vertical   |   viability.  |  model is in |         |
|            |              |               |   real-world |   ----  |
|            | take-off and |  ------------ |   settings.  |         |
|            |   landing    |               |   ----       |         |
|            |   (eVTOL)    |               | ------------ |         |
|            |   ai         |  ------------ |              |         |
|            | rcraft using |               |   ----       |         |
|            |   an         |   ----------  | ------------ |         |
|            |              |               |              |         |
|            | optimization |   ----------  |   ---------  |         |
|            |   model and  |               |              |         |
|            |              |               |   ---------  |         |
|            | simulations. |               |              |         |
|            |   --         |               |              |         |
|            | ------------ |               |              |         |
|            |              |               |              |         |
|            |   --         |               |              |         |
|            | ------------ |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |   ----       |   -           |   -          |   -     |
| ---------- | ------------ | ------------- | ------------ | ------- |
|   Ayyala   |   Est        |   Relies on   |   Heavy      |         |
| somayajula | imates drone |   population  |              |  United |
|   et       |   (UAS       |               |  reliance on |         |
| al. (2020) | ) demand for |  demographics |   expert     |  States |
|   -------- |   various    |               |              |   -     |
| ---------- |              | and the costs | opinions may | ------- |
|            | applications |   o           |   introduce  |         |
|   -------- |   through a  | f alternative |   b          |   -     |
| ---------- |   so         |   delivery    | ias, and the | ------- |
|            | cio-economic |   methods,    |              |         |
|   -------  |   an         |   heavily     |  assumptions |   ----  |
|            | alysis model |               |   may not    |         |
|   -------  |   that       |  depending on |   accurately |   ----  |
|            |              |   expert      |   reflect    |         |
|            | incorporates |               |   actual     |         |
|            |   expe       |  assumptions. |   demand.    |         |
|            | rt input and |   -           |   -          |         |
|            |              | ------------- | ------------ |         |
|            |  analysis of |               |              |         |
|            |   so         |   -           |   -          |         |
|            | cio-economic | ------------- | ------------ |         |
|            |   factors.   |               |              |         |
|            |   ----       |   ----------  |   ---------  |         |
|            | ------------ |               |              |         |
|            |              |   ----------  |   ---------  |         |
|            |   ----       |               |              |         |
|            | ------------ |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |   ----       |               |   -          |   -     |
|   Becker   | ------------ | ------------- | ------------ | ------- |
|   et al.   |   Us         |               |              |         |
|   (2018)   | es a gravity | Involves data | Assumes that |  Global |
|   -------- |   mode       |   on          |   factors    |   -     |
|            | l to predict |   population, |   a          | ------- |
|   -------- |   future air |   GDP,        | ffecting air |         |
|            |   pass       |               |   passenger  |   -     |
|   -------  | enger demand | distance, and |   demand are | ------- |
|            |   based on   |   ticket      |   similar to |         |
|   -------  |   so         |   prices,     |   those for  |   ----  |
|            | cio-economic |   assuming    |   drone      |         |
|            |              |               |              |   ----  |
|            |  and spatial | these factors |  deliveries, |         |
|            |   fa         |   also        |   w          |         |
|            | ctors, which |   influence   | hich may not |         |
|            |   coul       |   drone       |              |         |
|            | d be adapted |   delivery    | be accurate. |         |
|            |   for drone  |   demand.     |   -          |         |
|            |   delivery   |               | ------------ |         |
|            |              | ------------- |              |         |
|            |  estimation. |               |   -          |         |
|            |   ----       |               | ------------ |         |
|            | ------------ | ------------- |              |         |
|            |              |               |   ---------  |         |
|            |   ----       |   ----------  |              |         |
|            | ------------ |               |   ---------  |         |
|            |              |   ----------  |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |   ------     |   --          |              |   ---   |
|   Gunady   | ------------ | ------------- | ------------ | ------- |
|   et al.   |   Est        |               |              |   C     |
|   (2022)   | imates daily | Utilizes data |  Census data | hicago, |
|   -------- |   packag     |               |   may be     |   USA   |
|            | e demand for | on population |              |   ---   |
|   -------- |              |   de          |  outdated or | ------- |
|            |  middle-mile | nsity, income |   lack       |         |
|   -------  |   deli       |   le          |   precision, |   ---   |
|            | very using a | vels, housing |   which can  | ------- |
|   -------  |   popu       |   types, and  |   affect the |         |
|            | lation-based |               |              |   ----  |
|            |              | demographics, |  accuracy of |         |
|            | model at the |   as          |   the demand |   ----  |
|            |              | suming census |   estimates. |         |
|            | census tract |   data is     |              |         |
|            |   level,     |   accurate.   | ------------ |         |
|            |   i          |   --          |              |         |
|            | ncorporating | ------------- |              |         |
|            |   so         |               | ------------ |         |
|            | cio-economic |   --          |              |         |
|            |   variables. | ------------- |   ---------  |         |
|            |   ------     |               |              |         |
|            | ------------ |   ----------  |   ---------  |         |
|            |              |               |              |         |
|            |   ------     |   ----------  |              |         |
|            | ------------ |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+
|   -------- |   ---        |               |   ---        | Los     |
|   Jaller   | ------------ |  ------------ | ------------ | A       |
|   et al.   |              |   Uses        |              | ngeles, |
|   (2020)   | Assesses the |   e-commerce  | Assumes that | USA     |
|   -------- |              |   consumer    |   enhancing  |         |
|            | economic and |   behavior    |   last-mile  |         |
|   -------- |   e          |   data and    |   delivery   |         |
|            | nvironmental |   logistics   |   eff        |         |
|   -------  |   impacts of |   data,       | iciency will |         |
|            |              |   assuming    |   s          |         |
|   -------  |  residential |   that        | ignificantly |         |
|            |   deliveries |   last-mile   |              |         |
|            |   using an   |   efficiency  | reduce costs |         |
|            |   analytical |   directly    |   an         |         |
|            |   mod        |   impacts     | d emissions, |         |
|            | el, focusing |   outcomes.   |   w          |         |
|            |   on how     |               | hich may not |         |
|            |   imp        |  ------------ |   a          |         |
|            | rovements in |               | lways be the |         |
|            |   last-mile  |               |   case.      |         |
|            |              |  ------------ |   ---        |         |
|            | delivery can |               | ------------ |         |
|            |              |   ----------  |              |         |
|            | affect costs |               |   ---        |         |
|            |   an         |   ----------  | ------------ |         |
|            | d emissions. |               |              |         |
|            |   ---        |               |   ---------  |         |
|            | ------------ |               |              |         |
|            |              |               |   ---------  |         |
|            |   ---        |               |              |         |
|            | ------------ |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
|            |              |               |              |         |
|            |   ---------  |               |              |         |
+------------+--------------+---------------+--------------+---------+

# Factors driving demand for Drone Delivery

Numerous studies have modeled last-mile delivery demand to optimize
logistics operations, reduce costs, and improve service levels. These
models incorporate various factors such as demographic characteristics,
consumer behavior, spatial distribution, and temporal variation. For
instance, Boyer et al. (2009) examined the impact of consumer
demographics and attitudes on the choice of home delivery versus
in-store pickup. They found that income level, age, and technological
familiarity significantly influence delivery preferences. Hsiao et al.
(2009) analyzed consumer motivations for online shopping and found that
convenience and time-saving are primary drivers, suggesting a potential
increase in demand for efficient delivery services. In the context of
urban freight transport, Dablanc et al. (2013) studied the impact of
e-commerce on urban logistics, highlighting the challenges of increased
delivery traffic and the need for sustainable solutions. They emphasized
the importance of understanding spatial and temporal demand patterns to
optimize delivery routes and reduce environmental impacts.

We identified two demand drivers that can be mapped: household income
and population density. Wang et al. (2023) discuss the role of income on
a consumer's choice of delivery mode (attended/unattended home delivery,
automated self-collection locker, attended pickup point, and
click-and-collect); they found that higher income level corresponds to
higher probability of choosing home delivery. Higher-income households
were more inclined to opt for online deliveries during COVID-19
(Unnikrishnan and Figliozzi, 2020). This effect persisted after
COVID-19, with a follow-up study by Unnikrishnan and Figliozzi (2021)
finding that individuals with higher incomes had a greater likelihood of
making more home deliveries compared to before COVID-19 . Spurlock et
al. (2020) found that families with higher income were more likely to
receive deliveries across all item types. For a given week, they found
that the probability that a high-income household had at least one
delivery was 44% higher compared to a lower-income household. Kim (2020)
studied consumer preference for drone delivery and traditional delivery,
and found that consumers who earn a high income prefer the faster but
more expensive drone delivery service. German et al. (2018) considered
potential demand in California for package delivery by electric vertical
takeoff and landing (eVTOL) aircraft; assuming demand for eVTOL service
would be higher in areas with higher income because more customers would
be able to afford the premium for faster service. Gunady et al. (2022)
uses income, along with other socio-economic factors, as a metric to
estimate daily package order demand for middle-mile delivery with eVTOL
vehicles in Chicago.

Higher population density is likely to be associated with higher drone
delivery demand. Higher population density correlates with increased
urbanization levels (Singleton et al., 2016). In urban areas, residents
tend to have higher education and higher technology familiarity. Denser
urban populations tend to make more online orders (Farag et al., 2006;
Sylvia and Wang 2021; Cheng et al., 2021; Zhou and Wang, 2014; Locasciom
et al. 2016).

Finally, time of day affects demand. Residential deliveries are likely
to peak during the evening hours, when recipients are most likely to be
at home. In contrast, commercial deliveries may peak during regular
business hours, particularly around noon, as office workers place lunch
orders.

~~Higher population density can make drone delivery more cost-effective
(Ayyalasoyajula, 2020). Drone delivery faces challenges related to
battery life and flight range. Densely populated areas allow for shorter
delivery distances and more deliveries per flight, optimizing drone
utilization and potentially lowering the cost per delivery~~

~~densely populated cities often face severe traffic congestion, making
ground-based delivery slow and unpredictable. Drones offer a solution by
operating in a separate airspace, bypassing road networks and delivering
goods more quickly and reliably (Benarbia, 2021).~~

# Method

## Model Requirements

The primary objective of our market demand model is to quantify and map
the potential demand for drone delivery services across different
locations.

1.  The model shall incorporate market demand variables identified in
    existing literature, specifically: geographical features, temporal
    factors (e.g., peak delivery times), and demographic characteristics
    (e.g., median household income, population density).

2.  The model shall input data from open-source repositories, including
    but not limited to the U.S. Census Bureau and OpenStreetMap,
    covering all geographic regions within the United States. Data
    selection needs to prioritize comprehensiveness and reliability,
    ensuring that data sources are robust and up to date.

3.  The model shall generate demand estimates at the finest feasible
    spatial resolution, i.e., individual buildings, to allow precise
    prediction and mapping of drone deliveries.

## Scope & Key Assumptions

-   Focus on last-mile parcel delivery: This study will consider only
    domestic last-mile parcel deliveries within the United States.

-   Package weight: We will focus on packages weighing under 5 lbs.
    Amazon Prime Air claim to focus their design efforts on transporting
    5 lbs. over 10 km (Doole, 2020). (D'Andrea, 2014) also claims \<5
    lbs. to be optimal design requirement with respect to operating
    costs. According to Amazon, 86 percent of parcels delivered are
    below 5 lbs. (Pierce, 2013).

-   Delivery Urgency: While research of drone delivery in urgent medical
    applications is prominent, this paper focuses on commercial,
    non-medical deliveries.

-   One-directional delivery flow: We are only considering the flow from
    supplier to customer, no returns.

## Proposed Model

This section introduces the model we developed to map the estimated
demand for drone delivery.

Our study presents an analytical framework to predict potential demand
for drone deliveries at a fine spatial resolution---at the individual
building level---and across various temporal scales (hourly, daily,
monthly). By integrating geospatial data from OpenStreetMap (OSM) with
demographic information from the U.S. Census Bureau, we develop
probabilistic models that account for multiple factors influencing drone
delivery demand. These factors include building characteristics,
population demographics, accessibility, temporal variations, proximity
to stores, and building heights.

## Data Sources

We used two primary sources of data: OpenStreetMap (OSM) and the U.S.
Census.

### OpenStreetMap (OSM) Data

OSM, sometimes referred to as "Wikipedia of maps", provides freely
available crowdsourced geospatial data. We used the following:

-   **Building Footprints**: Geometries and attributes of individual
    buildings.

-   **Land Use Data**: Classification of buildings and land parcels into
    residential, commercial, industrial, and other categories, based on
    crowdsourced tags.

-   **Building Height Data**: Where available, we interpret building
    heights from OSM tags. For buildings without user-input height
    value, we estimate the height using k-nn method.

We used the osmnx Python library to download and process OSM data for
the study area.

### U.S. Census Data

We obtained demographic and socioeconomic data from the U.S. Census
Bureau:

-   Population Statistics: Total population, population density, age
    distribution at the census block or block group level.

-   Household Information: Number of households, household sizes, median
    income levels.

-   Economic Indicators: Employment rates, industry sectors.

**U.S. Census Population Variables:**

Total Population**:**

Total population in the census block. Needed for estimating the number
of potential consumers in each area.

> ACS Variable ID: B01003_001E.

Population by Age**:**

Number of individuals in specific age groups. Age distribution affects
consumer behavior and delivery demand patterns.

> Variable IDs:

-   Under 18 years: B01001_003E to B01001_006E (male), B01001_027E to
    B01001_030E (female)

-   18 to 34 years: B01001_007E to B01001_010E (male), B01001_031E to
    B01001_034E (female)

-   35 to 64 years: B01001_011E to B01001_019E (male), B01001_035E to
    B01001_043E (female)

-   65 years and over: B01001_020E to B01001_025E (male), B01001_044E to
    B01001_049E (female)

Income Variables

Median Household Income. Income levels influence purchasing power and
probability of ordering fast delivery services.

> Variable ID**: B19013_001E**

Housing Variables

Total and Occupied Housing Units**.** Number of housing units in the
census block. Helps in estimating the number of potential customers on
the ground.

> ACS Variable IDs**: B25001_001E, B25002_002E**

Employment Variables

> Employment status of residents aged 16 and over. Employment status may
> influence delivery demand due to income and time availability.
>
> ACS Variable IDs: B23025_002E (labor force), B23025_003E (employed),
> B23025_005E (unemployed)

We use API reference to access U.S. Census data. We import the data into
Python using the census, pandas, and geopandas libraries.

## Temporal Units

We define the following temporal units for analysis: hours \[0--23\],
days \[Monday--Sunday\], months \[January--December\].

## Land Use Classification

We need a consistent method of classification of real-life locations for
estimating drone delivery demand more precisely. For instance, we can
identify and exclude locations that we know are much less likely to
serve as commercial drone delivery destinations (e.g., industrial
buildings). There are several datasets available online to classify land
use:

## Possible ways to discretize and classify land use 

### Zoning codes

Zoning codes in the United States are a set of rules that determine what
can be built on a piece of land. They are established and enforced by
local governments and municipalities. Zoning codes are made up of
letters and numbers that indicate the type of use allowed for a specific
area. For example, R stands for residential, C stands for commercial,
and I stands for industrial. A number may be added to the letter to
specify the use of the land or the amount of space allowed. For example,
R-3 might allow high-rise residential buildings, while C-1 might
indicate low-rise commercial development.

For our application, zoning codes are not suitable for the following two
reasons: 1. Resolution: zoning areas span areas larger than individual
buildings. 2. Locality: There is no universal standard for zoning
classifications, cities designate their own zoning codes. Each local
government, such as a city, county, or municipality, has authority over
their zoning codes. This makes the development of an algorithm that will
work on the whole of the U.S. more challenging. Taking into account the
fact that local governments can also change their zoning code,
future-proof solutions are more difficult. The final reason why zoning
codes are not suitable for our solution is that people/institutions
change the designated zoning of land parcels, to take benefit on tax
breaks and legal loopholes.

To offer an alternative solution for future research, one could combine
zoning codes with building footprints (obtained from a different
source). However, keep in mind that this solution would be local to the
chosen area, since, as previously mentioned, zoning codes vary depending
on local authorities. Additionally, one could use ML and/or LLM
technology to interpret different zoning codes for their own algorithm.

### Regrid Parcel Data

Regrid is a commercial dataset service that provides detailed
parcel-level data. Regrid claim their dataset covers over 156 million
parcel boundaries and account for 99% of the US. Regrid's land parcel
data is quite detailed -- most land parcels include enough information
to deduce their main function: street address, local zoning code, land
use, measurements, etc.

Data is available to download, as well as through the use of API.

Regrid has limitations when used in our context: Regrid data is not free
-- hence, building a scalable model is costly. Another limitation is
that land parcel boundaries are not the same as building boundaries.
Land parcels can include many buildings. Examples include large housing
complexes, or college campuses, where multiple buildings are under one
parcel unit. Since our model requires a high-resolution method, we are
interested in buildings, so land parcel borders are of no use to us.

In the United States, zoning codes are not federally standardized. Each
local government, such as a city, county, or municipality, has authority
over their zoning codes. This makes the development of an algorithm that
will work on the whole of the U.S. more challenging. Taking into account
the fact that local governments can also change their zoning code,
future-proof solutions might include ML or LLM-based tools to interpret
zoning codes.

### Open Buildings 2.5D

The Open Buildings 2.5D Temporal Dataset by Google contains data about
building presence, fractional building counts, and building heights at
an effective spatial resolution of 4m, at an annual cadence from
2016-2023. It is produced from open-source, low-resolution imagery from
the Sentinel-2 satellite data. This dataset was built by Google Research
Africa team using AI, and is meant to provide critical information for
governments, organizations, and researchers working on population
growth, urban planning, and resource allocation.

While Open Buildings 2.5D can provide excellent building boundaries as
well as building heights, the dataset does not help with qualitative
classification of buildings by land use. So it would need to be combined
with another data source to classify by land use.

In any case, this dataset would not be suitable for our purposes,
because it does not include United States. Open Buildings 2.5D spans
Africa, South Asia, South-East Asia, Latin America and the Caribbean.

### OpenStreetMap Tags

OpenStreetMap (OSM) is a collaborative project that creates a free,
editable map of the world. It is built by a community of users who
contribute and maintain data about roads, buildings, land use, and much
more. OSM uses a system of tags -- key-value pairs assigned to map
elements to describe the characteristics of geographic features. These
tags can specify building types and functions.

For our application, OSM tags are the most suitable method for land use
classification for the following reasons. First, OSM offers
high-resolution data at the individual building level. Second, OSM is
freely available and regularly updated by the user community, making it
a cost-effective and future-proof data source. Another positive factor
is that, as previously mentioned, OSM contains building footprints as
well. Based on OSM tag info website, at the time of writing, there's
more than 620 million building footprints available for use.

Therefore, OSM tags are our preferred choice for classifying land use in
our model due to their granularity, accessibility, and consistency.

One limitation is that accuracy and completeness of OSM data can vary
depending on location. Major urban centers have detailed building data,
while rural or suburban areas' coverage is not as good. Despite this,
OSM remains the most effective tool for our purposes due to its
comprehensive coverage and the level of detail it provides at the
building level.

## Chosen Building Classification Framework using OSM Tags.

\[add chatgpt classification here\]

We categorize buildings into the following classes based on their
expected role in drone deliveries:

**Delivery Origins (DO)**: Buildings likely to serve as starting points
for deliveries, such as warehouses, distribution centers, retail stores,
and restaurants.

-   Commercial Buildings: Structures used for business activities,
    including retail outlets, warehouses, and shops.

> Tags: building=warehouse, building=retail, building=shop,
> building=supermarket, building=convenience store, building=Walmart,
> building=Target, building=CVS, shop=supermarket, amenity=cafe,
> amenity=fast_food

**Delivery Destinations (DD)**: Buildings likely to receive deliveries,
primarily residential dwellings and offices. Places that people indicate
as delivery addresses.

-   Residential Buildings: Structures primarily used for dwelling
    purposes.

> Tags: building=house, building=apartments, building=residential,
> building=detached, building=semidetached_house

-   Office Buildings: Structures primarily used as office space for
    people to work.

> Tags: building=office, amenity=coworking_space, office=coworking,
> office=\*

**Unlikely Destinations (UD)**: Buildings unlikely to be involved in
drone deliveries, such as industrial facilities, agricultural buildings,
and utilities.

-   Industrial, Agricultural, Utility, Infrastructure:

> Tags: building=industrial, building=manufacture, building=hangar,
> building=barn, building=stable, building=farm_auxiliary,
> building=service, building=transformer_tower, amenity=power_station

## Handling Multiple and Conflicting Tags

## Data Preprocessing

In this section, we describe the steps involved in preprocessing and
integrating data from OpenStreetMap and the U.S. Census Bureau to
prepare it for computational demand estimation.

## Spatial Alignment

When working with geospatial data, to achieve accurate integration, it's
important to project your data to a common coordinate reference system
(CRS). OSM uses the World Geodetic System 1984 (WGS 84) coordinate
reference system, also known as EPSG 4326.

The U.S. Census data is typically provided in the North American Datum
of 1983 (NAD83) coordinate system.

For future merging of OSM and Census data, we project both to EPSG 4326.

## Data Integration

We used spatial joins to associate each building footprint from OSM with
the corresponding census tract or block from the U.S. Census data. This
allowed us to link demographic information to individual buildings. We
performed the spatial join using geopandas.sjoin() function.

## Estimating Building Attributes

## Estimating Building Footprint Area

We calculated the footprint area $A_{footprint}$ of each building using
the geometry of the building polygons provided by OSM.

## Estimating Building Height

Building height is needed for estimating building volume, which in turn
influences population allocation.

For each building, the number of floors $N_{floors}$ was extracted from
the building:levels tag in OSM data. The building height was extracted
from building:height tag in OSM.

If any of these information was missing:

-   If building height is known:

    -   we divide building height by assumed average floor height -- 3
        meters, and round to the nearest integer.

-   If number of floors is known:

    -   correspondingly, we multiply $N_{floors}$ by assumed average
        floor height -- 3 meters, and round to the nearest integer.

-   If neither $N_{floors}$ nor $Height$ is known:

    -   for each building without any height data, we use the
        k-Nearest-Neighbors (k-NN) method. We identify 5 nearest
        buildings with known height data. We then calculate the
        arithmetic average of the known heights, and assume the
        calculated value on the building without known height.

## Handling User-Selected Areas

We want to set up our model such that it would work with a custom Area
of Interest (AoI) selected by a user. When a user selects an area that
overlaps multiple census blocks or represents a fraction of a block, we
face challenges in population allocation due to the spatial mismatch
between the selected area and census boundaries.

-   If the user selects a fraction of Census unit:

We use areal interpolation to proportionally allocate the population
from census tracts to the user-selected area based on the spatial
overlap. The population assigned to the user-selected area of interest
$P_{AOI}\ $is calculated using the following formula:

$$P_{AOI} = P_{tract} \times (\frac{A_{overlap}}{A_{tract}})$$

> Where:

-   $P_{tract}$: Total population of the census tract.

-   $A_{overlap}$: Area of overlap between the user-selected area and
    the census block.

-   $A_{tract}$: Total area of the census block.

> Assumption: Proportional Allocation -- we assume the population is
> uniformly distributed within the census tract.

-   If the user selects an area that overlaps multiple census tracts:

We use areal interpolation to proportionally allocate the population
from census tracts to the user-selected area based on the

$$P_{AOI} = \sum_{n = 1}^{n}{P_{tract,\ i} \times \left( \frac{A_{overlap,\ i}}{A_{tract,i}}\  \right)}$$

> Where:

-   *n:* Number of census tracts overlapping the user-selected area.

-   $P_{tract,\ i}$: Population of the *i*-th census tract

-   $A_{overlap,\ i}$: Overlap area between the user-selected area and
    the *i*-th census tract

-   $A_{tract}$: Total area of the census block.

> Assumption: Proportional Allocation -- we assume the population is
> uniformly distributed within the census tract.

## Allocating Population to Buildings within Area of Interest

To distribute the population within the user-selected area to individual
buildings, we take the following steps:

First, we sort out only residential buildings, based on OSM tags. For
each residential building *j* within the user-selected area, compute the
building volume:

-   Calculate building volumes within Area of Interest**:**

For each building *j* within the user-selected area, compute the
building volume:

$$V_{j} = A_{footprint} \times H_{j}$$

-   Compute total building volume:

Sum the volumes of all buildings within the user-selected area:

$$V_{total} = \sum_{j}^{}V_{j}$$

-   Allocate population to each building:

Assign population to each building *j* based on its proportion of the
total volume:

$$P_{j} = P_{area} \times (\frac{V_{j}}{V_{total}})$$

Assumptions:

-   Population is distributed proportionally to the volume of
    residential buildings.

-   Only residential buildings are considered for population allocation.

    1.  ## Adjusting for Occupancy Rates

To refine the population estimates, we adjust for occupancy rates using
housing data from the ACS. This way we account for vacant units,
providing a more accurate estimate of the actual resident population
likely to generate delivery demand.

$$O_{rate} = \frac{Occupied\ Housing\ Units}{Total\ Housing\ Units}$$

-   Hence, adjusted population for building *j*:

$$P_{adj,j} = P_{j} \times O_{rate}$$

## Demand Estimation

The demand estimation step is where all the processed data and
identified factors come together to quantify the expected number of
drone deliveries for each building over time. We aim to model the demand
as a stochastic process, accounting for spatial and temporal variations
influenced by income, population density, building type, and temporal
factors such as time of day and day of the week.

**Modeling Approach**

We model the demand for drone deliveries at each building using a
Poisson distribution, a common choice for modeling count data
representing the number of events occurring within a fixed interval of
time or space. The Poisson distribution is appropriate because: Events
are independent -- the occurrence of a delivery at one building does not
affect deliveries at other buildings. The probability of a delivery
occurring is proportional to the length of the time interval. Individual
delivery events are relatively rare compared to the possible number of
events.

The expected number of deliveries (λ) for each building is influenced by
several factors:

-   Income Level: Higher income levels correlate with higher delivery
    demand.

-   Population Allocation: More occupants in a building increase the
    likelihood of deliveries.

-   Building Function: Residential and office buildings have different
    demand patterns.

-   Temporal Factors**:** Demand varies by time of day, day of the week,
    and season.

-   Proximity to Retail: Buildings closer to retail outlets may have
    higher demand due to shorter delivery times.

**Expected Demand per Building**

The expected demand (λ) for drone deliveries at building j during time
interval t is modeled as:

$$\lambda_{j,t} = \beta_{o} \times f(I_{j},P_{adj,j},B_{j},D_{j}) \times g(T_{t})$$

\*\*\*OLD STUFF, IGNORE PLEASE\*\*\*

# Sensitivity Analysis

(still need to code this)

*(For one intance: Graphs or tables showing how changes in the logistic function
parameters (L, k, x0) impact the estimated demand.
And so on, but with all other 'choices', both micro and macro level choices that we've been making.)*

For one instance: We conducted a
sensitivity analysis on key parameters:

1.  Maximum orders per month (L): Varied L by +/- 20%

2.  Growth rate (k): Tested k values 20% higher and lower

3.  Income midpoint (x0): Adjusted x0 by +/- \$10,000

# Case Study: Austin, Texas

{In this section, we provide a case study of Austin, Texas}

Conclusion

Application to other countries:

US is good and bad at the same time. It's very good with data and its
agencies, and it's not corrupt and takes data integrity seriously. But
also, the laws of different states are different.

In other countries, the territory might be smaller and less diverse, but
their data digitalizaion, standartization and availability levels are not on the same level.

# Conclusion 

### Possible implications of wide-scale of drone delivery 

### Who will benefit from drones the most?

From an engineering perspective, those who need it the most -- i.e., the
most polluted, and hard-to-navigate, congested, cities. (Istanbul,
New-York, Mocow, Tokyo, Beijing, Dubai. And then most polluted too.)

1.  # Job loss

2.  # Initial 'baby diseases' 

# Future Work 

If you want to do a custom solution for your town, definitely consider
using things like zoning data to enhance your data. You could also use
AI agents to analyze this.

Same for lcoations, consider using an AI bot to search for Wikipedia or
other web sources of average building height, list of tallest buildings,
etc.

# References

Jones, E. (2024, August 1). *Expect more drone deliveries in North Texas
soon*. CBS News.
https://www.cbsnews.com/texas/news/expect-more-drone-deliveries-in-north-texas-soon/

Koch, S. and Klein, R., "Route-based approximate dynamic programming for
dynamic pricing in attended home delivery," European Journal of
Operational Research, Vol. 287, Iss. 2, pp. 633-652, 2020.

<https://www.sciencedirect.com/science/article/pii/S0377221720303209?via%3Dihub>

Narkus-Kramer, M., "Future Demand and Benefits for Small-Autonomous
Unmanned Aerial Systems Package Delivery," AIAA Aviation Technology,
Integration, and Operations Conference, 2017.

<https://arc.aiaa.org/doi/pdf/10.2514/6.2017-4103>

Cheng, C., Sakai, T., Alho, A., Cheah, L., and Ben-Akiva, M., "Exploring
the Relationship between Locational and Household Characteristics and
E-Commerce Home Delivery Demand, Logistics, Vol. 5, Iss. 2, 2021.

<https://www.mdpi.com/2305-6290/5/2/29>

Santana-Jimenez, Y. and Hernandez, J. M., "Estimating the effect of
overcrowding on tourist attraction: The case of Canary Islands, Tourism
Management, Vol. 32, Iss. 2, 2011, pp. 415-425.

<https://www.sciencedirect.com/science/article/pii/S0261517710000609?via%3Dihub>

\[\] O'Hara, J. K. and Lin, J., "Population Density and Local Food
Market Channels," Applied Economic Perspectives and Policy, Vol. 42,
Iss. 3, 2019, pp. 477-496.

<https://onlinelibrary.wiley.com/doi/10.1093/aepp/ppy040>

Bridgelall, R., "Forecasting market opportunities for urban and regional
air mobility," Technical Forecasting & Social Change, Vol. 196, 2023.

<https://www.sciencedirect.com/science/article/abs/pii/S0040162523005206?via%3Dihub>

\[\] Cohen, D., "Understanding Population Density," United States Census
Bureau, 2015.

<https://www.census.gov/newsroom/blogs/random-samplings/2015/03/understanding-population-density.html>

\[\] Kim, S. H., "Choice model based analysis of consumer preference for
drone delivery service," Journal of Air Transport Management, Vol. 84,
2020.

[https://www.sciencedirect.com/science/article/pii/](https://www.sciencedirect.com/science/article/pii/S0969699719304661?fr=RR-2&ref=pdf_download&rr=86e45588ef44b0b1)

\[\] Spurlock, C. A., Todd-Blick, A., Wong-Parodi, G., and Walker, V.,
"Children, Income, and the Impact of Home Delivery on Household Shopping
Trips," Journal of the Transportation Research Board, Vol. 2674, Iss.
10, 2020.

<https://journals.sagepub.com/doi/10.1177/0361198120935113>

\[\] Wang, X., Wong, Y. D., Shi, W., and Yuen, K. F., "An investigation
on consumers' preferences for parcel deliveries: applying consumer
logistics in omni-channel shopping," The International Journal of
Logistics Management, Vol. 35, Iss. 2, 2023.

[https://www.emerald.com/insight/content/doi/10.1108/](https://www.emerald.com/insight/content/doi/10.1108/IJLM-07-2022-0288/full/html?casa_token=Xw3uz7BBh5QAAAAA:c-G7UPOlYZu_FhatNzSDRx_7GS92LzijNwQ2Znyv-rhleD5vm0kGnDN5hMrI1HwQo6Zrtr4mqVJs-ZQ2L8cKSB93BTwws0F26dEtbf0UPdpdC-tZMaUAmA)

\[\] Nuzzolo, A., Coppola, P., and Comi, A., "Freight Transport
Modeling: Review and Future Challenges," International Journal of
Transport Economics, Vol. XL, No. 2, 2013.

<https://www.torrossa.com/en/resources/an/2626427>

\[\] Wang, X., Wong, Y. D., Teo, C. C., Yuen, K. F., and Feng, X., "The
four facets of self-collection service for e-commerce delivery:
conceptualisation and latent class analysis of user segments",
Electronic Commerce Research and Applications, Vol. 39 No. 1, 2020.

<https://www.sciencedirect.com/science/article/abs/pii/S1567422319300730>

\[\] Stone, R., "The Analysis of Market Demand," Oxford University
Press, Vol. 108, No. 3/4, 1945, pp. 286-391.

<https://www.jstor.org/stable/2981291>

\[\] Scott, M. P., "Income Definition: Types, Examples, and Taxes,"
Investopedia, 2023.

<https://www.investopedia.com/terms/i/income.asp>

\[\] Goyal, R., Reiche, C., Fernando, C., and Cohen, A., "Advanced Air
Mobility: Demand Analysis and Market Potential of the Airport Shuttle
and Air Taxi Markets," Advanced Air Mobility for Innovative and
Sustainable Transport, 2021.

<https://www.mdpi.com/2071-1050/13/13/7421>

\[\] Becker, K., Terekhov, I., Niklaß, M., Gollnick, V., "A global
gravity model for air passenger demand between city pairs and future
interurban air mobility markets identification," On-Demand Mobility
Markets and Demand, 2018.

<https://arc.aiaa.org/doi/abs/10.2514/6.2018-2885>

\[\] Ayyalasomayajula, S., Vlachou, K., and Zhang, L., "Small UAS Demand
Estimation," AIAA/IEEE Digital Avionics Systems Conference (DASC), 2020.

[https://ieeexplore.ieee.org/abstract/document/9256571](https://ieeexplore.ieee.org/abstract/document/9256571?casa_token=FcaaTfTD_0IAAAAA:CpE6bsZlKpYyko0kpv15rgISQkwWyMMiKcrxy53sXpPTLpWk3N8GASMIDW9GdTYiXnQQP4pFaZo)

\[\] Gunady, N. I., Sells, B. E., Patel, S. R., Chao, H., DeLaurentis,
D. A., and Crossley, W. A., "Evaluating Future Electrified Urban Air
Mobility Cargo Delivery Operations," AIAA Aviation Forum, 2022.

<https://arc.aiaa.org/doi/abs/10.2514/6.2022-3756>

\[\] German, B. J., Daskilewicz, M. J., Hamilton, T. K., and Warren, M.
M., "Cargo Delivery by Passenger eVTOL Aircraft: A Case Study in the San
Francisco Bay Area," AIAA SciTech Forum, 2018.

<https://arc.aiaa.org/doi/abs/10.2514/6.2018-2006>

\[\] Doole, M., Ellerbroek, J., and Hoekstra, J., "Urban airspace
traffic density estimation," SESAR Innovation Days, 2018.

<https://research.tudelft.nl/en/publications/drone-delivery-urban-airspace-traffic-density-estimation>

\[\] Brown, L. G., "Convenience in Services Marketing," Journal of
Services Marketing, Vol. 4, Iss. 1. 1990.

[[https://www.emerald.com/insight/content/doi/10.1108/EUM0000000002505/full/html]{.underline}](https://www.emerald.com/insight/content/doi/10.1108/EUM0000000002505/full/html)

\[\] Mortimer, C. J., "Two Keys to Modern Marketing," The Updegradd
Press, 1955, pp. 7-17.

\[\] Kelley, E.J., "The Importance of Convenience in Consumer
Purchasing," Journal of Marketing, Vol. 23, Iss. 1, 1958.

[[https://journals.sagepub.com/doi/10.1177/002224295802300105]{.underline}](https://journals.sagepub.com/doi/10.1177/002224295802300105)

\[\] Akartunali, K., Boland, N., Evans, I., Wallace, M., and Waterer,
H., "Airline planning benchmark problems---Part II: Passenger groups,
utility and demand allocation," Computers & Operations Research, Vol.
40, Iss. 3, 2013, pp. 793-804.

[[https://www.sciencedirect.com/science/article/pii/S0305054812000585]{.underline}](https://www.sciencedirect.com/science/article/pii/S0305054812000585?casa_token=ESJC1lHdJH0AAAAA:J5L55DLq0DIaNqCNJRJs_SriFS-tdlF4SxVsvZ_LfTlk6IuWlIY6BZflut6EHqlcCT3F7jKzgSU)

\[\] Lowe, J., "Demand, marketing, and time," European Journal of
Marketing, 1973.

[[https://www.emerald.com/insight/content/doi/10.1108]{.underline}](https://www.emerald.com/insight/content/doi/10.1108/EUM0000000005105/full/html)

\[\] Jellinek, S., "Consideration for a donation--economic aspects,"
National Library of Medicine, 2004, pp. 453-470.

[[https://pubmed.ncbi.nlm.nih.gov/15270481/]{.underline}](https://pubmed.ncbi.nlm.nih.gov/15270481/)

\[\] Zhang, J. J., Pease, D. G., Hui, S. C., Thomas, J. M., "Variables
affecting the spectator decision to attend NBA games," Sport Marketing
Quarterly, Vol. 4, 1995, pp. 29-39.

[[https://www.sid.ir/paper/576409/en#downloadbottom]{.underline}](https://www.sid.ir/paper/576409/en#downloadbottom)

\[\] Bansode, U. M., Kulkarni, P., Kedar, Y., Saravde, O., and Nikam,
K., "Automated Drone Delivery System," International Journal for
Research in Applied Science & Engineering Technology (IJRASET), Vol. 11,
Iss. 11, 2023.

[[https://www.ijraset.com/best-journal/automated-drone-delivery-system]{.underline}](https://www.ijraset.com/best-journal/automated-drone-delivery-system)

\[\] Fisher, M., Gallino, S., and Xu, J. J., "The Value of Rapid
Delivery in Omnichannel Retailing," Journal of Marketing Research, Vol.
56, Iss. 5, 2019, pp. 732-748.

[[https://journals.sagepub.com/doi/10.1177]{.underline}](https://journals.sagepub.com/doi/10.1177/0022243719849940)

\[\] Tarca, C., "Grow your business your way with Uber Eats," URL:
[[https://www.uber.com/blog/grow-delivery-business-uber-eats/]{.underline}](https://www.uber.com/blog/grow-delivery-business-uber-eats/#:~:text=For%20example%2C%203.5%20million%20active,less%20than%2030%20minutes%20globally)
\[retrieved 5 March 2024\].

\[\] DoorDash, URL:
[[https://www.doordash.com/food-near-me/]{.underline}](https://www.doordash.com/food-near-me/)
\[retreived 5 March 2024\]

\[\] Li, X., Tupayachi, J., Sharmin, A., and Ferguson, M. M.,
"Drone-Aided Delivery Methods, Challenge, and the Future:

A Methodological Review," The Applications of Drones in Logistics, Vol.
7, Iss. 3, 2023.

[[https://www.mdpi.com/2504-446X/7/3/191]{.underline}](https://www.mdpi.com/2504-446X/7/3/191)

\[\] Gatteschi, V., Lamberti, F., Parvati, G., Sanna, A., Demartini, C.,
Lisanti, A., and Venezia, G., "New Frontiers of Delivery Services Using
Drones: a Prototype System Exploiting a Quadcopter for Autonomous Drug
Shipments," IEEE Annual Computer Software and Applications Conference,
2015, pp. 920-927.

[[https://ieeexplore.ieee.org/document/7273724]{.underline}](https://ieeexplore.ieee.org/document/7273724)

\[\] Johannson

\[\] Salim

\[\] Bangeman, E., "Amazon begins drone deliveries in California and
Texas," URL:
[[https://arstechnica.com/gadgets/]{.underline}](https://arstechnica.com/gadgets/2022/12/amazon-begins-drone-deliveries-in-california-and-texas)/
\[retrieved 10 January 2024\]

\[\] Howarth, J., "Number of Amazon Prime Members (2023)," URL:
[[https://explodingtopics.com/blog/]{.underline}](https://explodingtopics.com/blog/amazon-prime-member-stats)
\[retrieved 10 January 2024\]

\[\] Alix Partners., "Consumers Are Getting More Impatient About
Delivery Times," URL: <https://www.marketingcharts.com/> \[retrieved 10
January 2024\]

\[\] Leonard, W., "Some Economic Considerations of Professional Team
Sports," Journal of Sports Behavior, Vol. 20, Iss. 3, 1997.

[[https://www.proquest.com/docview/215882803/fulltextPDF/]{.underline}](https://www.proquest.com/docview/215882803/fulltextPDF/6F201E91B4164D8BPQ/1?accountid=13360&sourcetype=Scholarly%20Journals)

\[\] Zhang, J. J., Lam, E. T. C., Connaughton, D. P., "General Market
Demand Variables Associated with Professional Sport Consumption,"
International Journal of Sports Marketing and Sponsorship, 2003.

<https://www.emerald.com/insight/content/doi/10.1108/IJSMS-05-01-2003-B003/full/html>

\[\]  Unnikrishnan, A. and Figliozzi, M., "A Study of the Impact of
COVID-19 on Home Delivery Purchases and Expenditures," Civil and
Environment Engineering Faculty Publications and Presentations, 2020.

[[https://pdxscholar.library.pdx.edu/]{.underline}](https://pdxscholar.library.pdx.edu/cengin_fac/557/)

\[\] Edwards, S. M., Lee, J. K., and Ferle, C. L., "Does Place Matter
When Shopping Online? Perceptions of Similarity and Familiarity as
Indicators of Psychological Distance," Journal of Interactive
Advertising, Vol. 10, Iss. 1, 2009.

[[https://www.tandfonline.com/doi/full/10.1080/]{.underline}](https://www.tandfonline.com/doi/full/10.1080/15252019.2009.10722161)

\[\] Dongp, F., "Is Geographic Location Unimportant for Online
Shopping," Research on Economics and Management, 2015.

[[https://www.semanticscholar.org/paper/]{.underline}](https://www.semanticscholar.org/paper/Is-Geographic-Location-Unimportant-for-Online-Dongp/9bc79e5b27dfbbfda9545b0752cf44b1054b790a)

\[\] Forman, C., Ghose, A., and Goldfarb, A., "Competition between Local
and Electronic Markets: How the Benefit of Buying Online Depends on
Where You Live," NET Institude Working Paper, No. 06-15, 2006.

[[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=941175]{.underline}](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=941175)

\[\] Vempati, L., Crapanzano, R., Woodyard, C., and Trunkhill, C.,
"Linear Program and Simulation Model for Aerial Package Delivery: A Case
Study of Amazon Prime Air in Phoenix, AZ," AIAA Aviation Technology,
Integration, and Operations Conference, 2017.

[[https://arc.aiaa.org/doi/epdf/10.2514/6.2017-3936]{.underline}](https://arc.aiaa.org/doi/epdf/10.2514/6.2017-3936)

\[\] Zhang, Z., Zhang, Z., and Chen, P., "Early Bird Versus Late Owl: An
Empirical Investigation of Individual Shopping Time Habit and its
Effects," MIS Quarterly, Vol. 45, No. 1, 2021, pp. 117-162.

 [[https://web.p.ebscohost.com/ehost/]{.underline}](https://web.p.ebscohost.com/ehost/pdfviewer/pdfviewer?vid=1&sid=a0f84e23-cc33-4d68-a6f4-83f804282a81%40redis)

\[\]  Unnikrishnan, A. and Figliozzi, M., "Exploratory analysis of
factors affecting levels of home deliveries before, during, and
post-COVID-19," Transportation Research Interdisciplinary Perspectives,
Vol. 10, 2021.

[[https://www.sciencedirect.com/science/]{.underline}](https://www.sciencedirect.com/science/article/pii/S2590198221001093)

\[\]  Singleton, A. D., Dolega, L., Riddlesden, D., and Longley, P. A.,
"Measuring the spatial vulnerability of retail centres to online
consumption through a framework of e-resilience," Geoforum, Vol. 69,
2016, pp 5-18.

[[https://www.sciencedirect.com/science/article/]{.underline}](https://www.sciencedirect.com/science/article/pii/S0016718515301500?via%3Dihub) 

\[\]  Farag, S., Weltevreden, J., Rietbergen, T., Dijst, M., and Oort,
F., "E-Shopping in the Netherlands: Does Geography Matter," Environment
and Planning B: Urban Analytics and City Science, Vol. 33, 2006.

[[https://journals.sagepub.com/doi/10.1068/]{.underline}](https://journals.sagepub.com/doi/10.1068/b31083)

\[\]  Locasciom, D., Levy, M., Ravikumar, K., Briceno, S., German, B.,
and Mavris, D., "Evaluation of Concepts of Operations for On-Demand
Package Delivery by Small Unmanned Aerial Systems," AIAA Aviation Forum,
2016.

[[https://arc.aiaa.org/doi/abs/10.2514/]{.underline}](https://arc.aiaa.org/doi/abs/10.2514/6.2016-4371)

\[\]  Fabusuyi, T., Twumasi-Boakye, R., Broaddus, A., Fishelson, J., and
Hampshire, R. C., "Estimating small area demand for online package
delivery," Journal of Transport Geography, Vol. 88, 2020.

[[https://www.sciencedirect.com/science/article/pii/]{.underline}](https://www.sciencedirect.com/science/article/pii/S0966692320309418?casa_token=UQG9wmzB8QcAAAAA:tjXQSPHGIJTDWdkQf45OvNcM6BLCsoyaKOFwYh7FfJRWqA9Gewq4_X3eLKpf0uKgCGS4dVhSEIk)

\[\]  Byon, K., et al., "Identifying Key Market Demand Factors
Associated with High School Basketball Tournaments," URL:
[[https://scholarworks.gsu.edu/kin_health_facpub/20/]{.underline}](https://scholarworks.gsu.edu/kin_health_facpub/20/)
\[retrieved 23 January 2024\]

\[\]  Proussaloglou, K., Koppelman, F., "Air carrier demand".
Transportation 22, 371--388 (1995).
[[https://doi.org/10.1007/BF01098165]{.underline}](https://doi.org/10.1007/BF01098165)
\[retrieved 10 January 2024\]

\[\]  Saad, A., "Factors affecting online food delivery service in
Bangladesh: an empirical study," URL:
[[https://www.emerald.com/insight/content/doi/10.1108/BFJ-05-2020-0449/full/html]{.underline}](https://www.emerald.com/insight/content/doi/10.1108/BFJ-05-2020-0449/full/html)
\[retrieved 15 January 2024\]

\[\]  Sylvia, H., Wang, Z., "Impacts of food accessibility and built
environment on on-demand food delivery usage," URL:
[[https://www.sciencedirect.com/science/article/abs/pii/S1361920921003151]{.underline}](https://www.sciencedirect.com/science/article/abs/pii/S1361920921003151)
\[retrieved 16 January 2024\]

*Spatially explicit Definition \| Law Insider*. (n.d.). Law Insider.
https://www.lawinsider.com/dictionary/spatially-explicit#:\~:text=Spatially%20explicit%20means%20that%20a%20geographic%20feature,be%20recorded%20and%20found%20on%20a%20map.

Kornatowski, P., Bhaskaran, A., Heitz, G. M., Mintchev, S., & Floreano,
D. (2018). Last-centimeter personal drone delivery: field deployment and
user interaction. IEEE Robotics and Automation Letters, 3(4), 3813-3820.
https://doi.org/10.1109/lra.2018.2856282

![Relationship between urban density and commercial freight deliveries
1 ](vertopal_662e792a08874e99abe09ac12aa0eb99/media/image1.png){width="2.6644083552055995in"
height="2.1568624234470692in"}

Rodrigue, Jean-Paul & Dablanc, Laetitia & Giuliano, Genevieve. (2017).
The Freight Landscape: Convergence and Divergence in Urban Freight
Distribution. Journal of Transport and Land Use. 10.
10.5198/jtlu.2017.869.

![A diagram of a freight and freight Description automatically
generated](vertopal_662e792a08874e99abe09ac12aa0eb99/media/image2.png){width="2.8333333333333335in"
height="1.3425032808398951in"}
https://transportgeography.org/contents/geography-city-logistics/diversity-urban-freight-activities/urban-density-mobility-commercial-freight-deliveries/

![A group of trucks and buildings Description automatically
generated](vertopal_662e792a08874e99abe09ac12aa0eb99/media/image3.png){width="3.25490157480315in"
height="1.2713593613298337in"}

We note that UAS cargo operations can be conceptually separated into
four segments, in context of the journey of a product from supplier to
the end consumer: first-mile, middle-mile, last-mile, and
last-centimeter delivery.

  ------------------------------------------------------------------------------------------
                 **First-mile delivery** **Middle-mile   **Last-mile     **Last-centimeter
                                         delivery**      delivery**      delivery**
  -------------- ----------------------- --------------- --------------- -------------------
  Definition     Transport of products   Transport of    Delivery of     Precision delivery
                 from a                  products from   goods from a    to the exact
                 manufacturer/supplier   warehouses or   local           location preferred
                 to warehouse or         distribution    distribution    by the customer,
                 distribution center.    centers to      center or       such as a specific
                                         retail stores   retail store    room in a home or a
                                         or secondary    directly to the backyard.
                                         distribution    consumer\'s     
                                         centers.        doorstep.       

  Conventional   Ship, Train, Truck      Train, Truck    Van,            Human (courier),
  Transport                                              Motorcycle,     potentially
  Methods                                                Bicycle, Human  automated
                                                         (courier)       technologies like
                                                                         robots

  Average        100-1000+ km            50-500 km       1-50 km         0-50 m
  Distance                                                               

  Average Cost   \$0.05-\$0.15           \$0.10-\$0.25   \$0.50-\$2.00   \$1.00-\$5.00
  per Meter                                                              

  Sources                                Gunady et al.                   Chen et al., 2020
                                         2020                            
  ------------------------------------------------------------------------------------------

Labor Costs

The delivery provider is an essential part of the supply chain.
Therefore, they are the most significant expenditures, amounting to
about 50-60% of last mile delivery expenses. The truck drivers who
deliver the goods from stores right to the customer's doorstep are the
most expensive..

The Bureau of Labor Statistics (US) reports that truck drivers' average
wage is about \$15.12 per hour and can range from \$9.43 to \$29.39.
Express deliveries are even more expensive, going to around \$25.10 per
hour. Increased customer demands mean more deliveries and an increase in
labor costs.![A graph of cost per package Description automatically
generated](vertopal_662e792a08874e99abe09ac12aa0eb99/media/image4.gif){width="6.5in"
height="3.55625in"}

<https://www.scdigest.com/ontarget/18-07-12-2.php?cid=14441>

![A graph with lines and dots Description automatically
generated](vertopal_662e792a08874e99abe09ac12aa0eb99/media/image5.png){width="3.225489938757655in"
height="1.9738899825021872in"}

<https://transportgeography.org/contents/chapter3/transport-costs/first-last-mile-cost/>

According to market research firm Insider Intelligence, the last-mile
delivery fee typically accounts for 53% of the overall cost. According
to data previously published by Statista, the average last-mile delivery
cost per package is \$10.1. With carriers increasing parcel shipping
fees, sellers are under constant pressure to find ways to reduce the
cost. <https://shipsage.com/understanding-last-mile-delivery-fees/>

-   Businesses usually foot 25% of last-mile expenses, but this
    percentage is rising as the cost of inefficient supply chains rises.

-   Unless last-mile delivery is optimized, profits could potentially
    decline by 26% in three years.

-   Most delivery drivers pocket around \$16 to \$24 per hour.

-   The average last-mile cost for a small package in high-density
    delivery can be around \$10; for low-density heavy packages, it is
    \$5

! Last mile delivery is getting costly.

<https://eliteextra.com/last-mile-delivery-costs-the-most-expensive-step-in-the-supply-chain/>

### 1. Lower average speeds = more time on the road, and fewer miles-per-gallon

When your drivers are delivering multiple packages to different
locations around a city, they have to use local roads.

Smaller delivery trucks and vans average [6.5 miles per gallon
(MPG)](https://afdc.energy.gov/data/10310) at a steady speed of 55 miles
per hour. If you handle deliveries in urban areas, 55 mph is not a
realistic average speed for your delivery fleet. How low it will drop
depends on the local road and traffic situation.

The need to decelerate, stop, and accelerate at rapid intervals has a
significant impact on both average speeds and fuel efficiency.

So not only do your drivers have to spend a lot more time on the road to
cover the same distance, but it also costs you more in gas.

### 2. More stops lead to more idling and downtime

Driving and dropping off packages in the city leads to a lot more idling
than other stages of shipping. With all the traffic lights, diverse
vehicles on the road, and winding streets, it's impossible to avoid.

On average, a delivery truck uses [0.84 gallons per
hour ](https://www.energy.gov/eere/vehicles/fact-861-february-23-2015-idle-fuel-consumption-selected-gasoline-and-diesel-vehicles)when
idling. Plus, you still have to pay your delivery drivers regardless of
whether they are standing still or moving.

### 3.  Failed deliveries

When you are distributing goods to fulfillment centers or supply chain
partners, you don't have to worry about failed deliveries.

When you are delivering products to the final customer, however, failed
deliveries are a massive part of the equation.

A single failed delivery [costs
\$17.78](https://postandparcel.info/93399/news/e-commerce/true-cost-implications-failed-deliveries/),
on average, and an astounding 5% of all last mile deliveries fail.
That's why [shipping
accuracy](https://optimoroute.com/shipping-accuracy/) is such an
important thing to prioritize, especially in [ecommerce
shipping](https://optimoroute.com/ecommerce-shipping/) since the
shipping experience is a critical customer touchpoint. (from
https://optimoroute.com/last-mile-delivery/ **)**

Ostermeier, M., Heimfarth, A., & Hübner, A. (2021). Cost‐optimal
truck‐and‐robot routing for last‐mile delivery. *Networks*, 79, 364 -
389. <https://doi.org/10.1002/net.22030>.

Shetty, A., Qin, J., Poolla, K., & Varaiya, P. (2022). The Value of
Pooling in Last-Mile Delivery. *2022 IEEE 61st Conference on Decision
and Control (CDC)*, 531-538.
<https://doi.org/10.1109/CDC51059.2022.9992742>.

Macioszek, E. (2017). First and Last Mile Delivery -- Problems and
Issues. , 147-154.
[https://doi.org/10.1007/978-3-319-62316-0_12.\\](https://doi.org/10.1007/978-3-319-62316-0_12.\)

Brown, J., & Guiffrida, A. (2014). Carbon emissions comparison of last
mile delivery versus customer pickup. International Journal of Logistics
Research and Applications, 17, 503 - 521.
<https://doi.org/10.1080/13675567.2014.907397>.

Jaller, M., Pineda, L., Ambrose, H., & Kendall, A. (2021). Empirical
analysis of the role of incentives in zero-emission last-mile deliveries
in California. Journal of Cleaner Production, 317, 128353.
<https://doi.org/10.1016/J.JCLEPRO.2021.128353>.

Catania, B. (2023, February 27). *Trending Now: Last-Mile Delivery
Expectations For 2023*. Forbes.
https://www.forbes.com/sites/forbestechcouncil/2023/02/24/trending-now-last-mile-delivery-expectations-for-2023/?sh=79c7433d5e8d

Applicable stuff:

Industry estimates:

Ibisworld

Statista:

MarketsAndMarkets:
<https://www.marketsandmarkets.com/Market-Reports/drone-package-delivery-market-10580366.html>

Grand View Research:
<https://www.grandviewresearch.com/industry-analysis/delivery-drones-market-report>

Roland Berger:
<https://www.rolandberger.com/en/Insights/Publications/Cargo-drones-The-future-of-parcel-delivery.html>

Mordor Intelligence:
<https://www.mordorintelligence.com/industry-reports/delivery-drones-market>

Tools & Projects:

-   **Global Demand Model**

-   Sponsors: NASA and the National Institute for Aerospace

-   From Virginia Tech

-   **Demand Forecast Model Development for Urban Mobility Concepts**

-   Sponsors: NASA and the National Institute for Aerospace

-   **UAS Demand Generation and Airspace Performance Impact Prediction:
    Phase 2**

-   Sponsor: NASA Langley\'s Aeronautical Systems Analysis Branch

-   **Demand Modeling and Airspace Peformance Ipact Prediction for
    Unmanned Aerial Systems\
    **Sponsor: Airport Corporate Research Program

-   **Transportation Systems Analysis Model (TSAM) Enhancements to
    Support Future Passenger and Aerospace Vehicle Demand Estimation for
    the Next Generation Air Transportation System**\
    Sponsor: NASA Langley Research Center

-   **Aviation Demand Modeling of the Next Generation Air Transportation
    System (NGATS)**\
    Sponsor: NASA Langley Research Center

Federal Highway Administration also made a project on Behavioral-Based
(or Agent-Based) National Freight Demand Modeling, though it's not in
public access

(<https://highways.dot.gov/research/projects/behavioral-based-or-agent-based-national-freight-demand-modeling>
)

Freight Analysis Framework by Bureau of Transportation Statistics
(<https://www.bts.gov/faf>).

DATA sources by FHWA \--
<https://ops.fhwa.dot.gov/freight/freight_analysis/data_sources/index.htm>

Census Transportation Planning Products-2016 is another resource that
can be useful.( <https://transportation.org/ctpp/>)

Goodman, R. W. 2005. "WhateverYou Call it, Just Don't Think of Last-Mile
Logistics, Last." Global Logistics and Supply Chain Strategies 9 (12):
46--51.

<https://medium.com/vida-engineering/updating-the-ultimate-cloud-native-building-footprints-dataset-6d4384cb93c4>
