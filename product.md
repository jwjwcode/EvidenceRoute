#product statement
EvidenceRoute is a evidece aware multi-modal task orchestration system for auditing long video according to a SOP under cost and latency requirements. Initially the system focus on long video and text SOP. Image modality will be added later. It outputs structured reports, which can be reviewed by human.

#problem
Long video auditing is slow and it lacks evidence to support the auditing results.

#targeted users
1.safety, complience and quality inspectors
2.human reviewers responsible for approving reports
3. AI/ML engineer responsible to select the models.

User stories:
As a safety, complience and quality inspector, I want to upload long video and SOP a so that an automatic auditing report can be generated.
As a report reviewer, I want to match the report and corresponding video segments so that the report is supported by evidence.
As a AI/ML engineer, I want to select AI models based on cost and accuracy requiments so that the system achieves best tradeoff between cost and performance.

#week1
Nongoals
do not train models
do not make final safety conclusion automatically
do not build complete web 
do not deploy cloud
do not become general visual agent
do not read railway videos.
