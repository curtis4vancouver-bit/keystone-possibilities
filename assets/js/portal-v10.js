
(function() {
  function injectPortalMasterStyles() {
    /* Styles served via browser-cached assets/css/portal-v10.css */
    return;
  }
  injectPortalMasterStyles();
})();

// ============================================================================
// 1. MULTI-JOB FACTORY GENERATOR (22 BC TRADES, 12 INSPECTIONS, 8 MATERIAL STAGES)
// ============================================================================
function buildFactoryTradesForJob(scale, startOffsetMonths) {
  const s = scale || 1.0;
  const r = (n) => Math.round((n * s) / 500) * 500;
  return [
    { id: 1, phase: "01", name: "Architecture (AIBC), Structural/Geotech Engineering & Municipal Building Permit", sub: "Studio Vance Architecture AIBC & Apex Structural P.Eng.", contact: "Marcus Vance, Architect AIBC", phone: "(604) 732-8812", startDate: "2026-06-01", endDate: "2026-06-19", contract: r(68000), billed: r(68000), gate: "Issued IFC Plans, Sealed Schedule B & Municipal Building Permit", status: "Completed", contractPdf: { name: "01_Architecture_Engineering_Permit_Contract_Signed.pdf", date: "2026-06-01" }, docs: ["01_Architecture_Engineering_Permit_Contract_Signed.pdf"], revisions: [] },
    { id: 2, phase: "02", name: "Land Survey (BCLS Pinning), Topographic Benchmarks & SPEA Tree Barrier", sub: "Sea-to-Sky Geomatics & Arbor", contact: "Ian McAllister, BCLS", phone: "(604) 892-4100", startDate: "2026-06-22", endDate: "2026-07-03", contract: r(18500), billed: r(18500), gate: "BCLS Siting Certificate & SPEA Tree Protection Fence", status: "Completed", contractPdf: { name: "02_BCLS_Survey_Subcontract_Signed.pdf", date: "2026-06-20" }, docs: ["02_BCLS_Survey_Subcontract_Signed.pdf", "Tree_Protection_Barrier_Signoff.pdf"], revisions: [] },
    { id: 3, phase: "03", name: "Geotechnical Borehole Investigation, Subgrade Bearing & Shoring Design", sub: "Thurber Geotechnical Engineering Ltd.", contact: "Dr. A. Tremblay, P.Eng.", phone: "(604) 984-4321", startDate: "2026-07-06", endDate: "2026-07-14", contract: r(24000), billed: r(24000), gate: "Geotechnical Schedule B & 300 kPa Bedrock Bearing Report", status: "Completed", contractPdf: { name: "03_Thurber_Geotechnical_ScheduleB_Signed.pdf", date: "2026-07-04" }, docs: ["03_Thurber_Geotechnical_ScheduleB_Signed.pdf"], revisions: [] },
    { id: 4, phase: "04", name: "BC Energy Step Code 4 & Zero Carbon EL-4 Whole-Building Thermal Modeling", sub: "E3 Eco Group Energy Advisors", contact: "Liam O'Connor, CEA", phone: "(604) 684-5588", startDate: "2026-07-15", endDate: "2026-07-21", contract: r(9500), billed: r(9500), gate: "HOT2000 Pre-Construction Step Code 4 Compliance Dossier", status: "Completed", contractPdf: { name: "04_E3_StepCode4_EnergyModeling_Signed.pdf", date: "2026-07-12" }, docs: ["04_E3_StepCode4_EnergyModeling_Signed.pdf"], revisions: [] },
    { id: 5, phase: "05", name: "Hazardous Materials Abatement, Site Security Hoarding & Silt Fencing", sub: "Squamish Environmental & Site Prep", contact: "Trevor Vance", phone: "(604) 898-4410", startDate: "2026-07-22", endDate: "2026-07-31", contract: r(22000), billed: r(22000), gate: "WorkSafeBC Notice of Project & ESC Silt Fence Pass", status: "Completed", contractPdf: { name: "05_Abatement_SiteHoarding_Signed.pdf", date: "2026-07-18" }, docs: ["05_Abatement_SiteHoarding_Signed.pdf"], revisions: [] },
    { id: 6, phase: "06", name: "Land Clearing, Demolition, Stripping & Bulk Earthworks Excavation", sub: "Alpine Rock Excavation Ltd", contact: "Grant Vance", phone: "(604) 898-3312", startDate: "2026-08-03", endDate: "2026-08-14", contract: r(68000), billed: r(68000), gate: "Subgrade Stripping & Bulk Excavation Export", status: "Completed", contractPdf: { name: "06_Alpine_Excavation_Contract_Signed.pdf", date: "2026-07-28" }, docs: ["06_Alpine_Excavation_Contract_Signed.pdf"], revisions: [] },
    { id: 7, phase: "07", name: "Rock Blasting, Hydraulic Micro-Splitting & Geotech Bedrock Anchors", sub: "Tantalus Drilling & Blasting", contact: "Dr. A. Tremblay, P.Eng.", phone: "(604) 984-4321", startDate: "2026-08-17", endDate: "2026-08-26", contract: r(44000), billed: r(44000), gate: "Thurber Schedule B Rock Bearing & 25M Epoxied Dowels", status: "Completed", contractPdf: { name: "07_Bedrock_Anchor_Subcontract_Signed.pdf", date: "2026-08-12" }, docs: ["07_Bedrock_Anchor_Subcontract_Signed.pdf", "Thurber_Geotech_Bearing_Pass.pdf"], revisions: [
      
    ] },
    { id: 8, phase: "08", name: "Civil Underground Utilities, Storm Retention & BC Hydro ES54 Ducts", sub: "Sea-to-Sky Civil Works Ltd", contact: "Wayne Stevenson (ES54)", phone: "(604) 848-9688", startDate: "2026-08-27", endDate: "2026-09-08", contract: r(96000), billed: r(96000), gate: "BC Hydro ES54 Mandrel & PMT Vault Inspection Pass", status: "Completed", contractPdf: { name: "08_Civil_ES54_Subcontract_Signed.pdf", date: "2026-08-22" }, docs: ["08_Civil_ES54_Subcontract_Signed.pdf", "ES54_Mandrel_Pass_Certificate.pdf"], revisions: [] },
    { id: 9, phase: "09", name: "Footing & Foundation Formwork + 15M/20M Seismic Rebar Cages", sub: "Black Tusk Formwork & Rebar", contact: "Marco Rossi", phone: "(604) 815-9022", startDate: "2026-09-09", endDate: "2026-09-22", contract: r(112000), billed: r(112000), gate: "Structural P.Eng. Pre-Pour Rebar & Simpson ATS Hold-Downs", status: "Completed", contractPdf: { name: "09_Formwork_Rebar_Contract_Signed.pdf", date: "2026-09-01" }, docs: ["09_Formwork_Rebar_Contract_Signed.pdf", "Apex_Rebar_Field_Review_Pass.pdf"], revisions: [] },
    { id: 10, phase: "10", name: "35 MPa Concrete Placing, Boom Pump & Foundation Wall Pour", sub: "Burnco Concrete & Coastal Placing", contact: "Devon K.", phone: "(604) 892-1105", startDate: "2026-09-23", endDate: "2026-09-30", contract: r(84000), billed: r(84000), gate: "28-Day 35 MPa Cylinder Break Test & Slump Log", status: "Completed", contractPdf: { name: "10_Concrete_Placing_Contract_Signed.pdf", date: "2026-09-15" }, docs: ["10_Concrete_Placing_Contract_Signed.pdf", "Cylinder_Break_35MPa_Report.pdf"], revisions: [] },
    { id: 11, phase: "11", name: "Dampproofing, Dimple Membrane, Weeping Tile & 98% Proctor Backfill", sub: "Pacific Shield Waterproofing", contact: "Tyler Vance", phone: "(604) 773-4410", startDate: "2026-10-01", endDate: "2026-10-06", contract: r(32000), billed: r(32000), gate: "Municipal Drain Tile & Geotech 98% SPD Compaction Pass", status: "Completed", contractPdf: { name: "11_Waterproofing_DrainTile_Signed.pdf", date: "2026-09-25" }, docs: ["11_Waterproofing_DrainTile_Signed.pdf"], revisions: [] },
    { id: 12, phase: "12", name: "Underslab Plumbing DWV, Radon Depressurization, XPS & Slab Pour", sub: "Garibaldi Concrete & Sea-to-Sky Plumbing", contact: "Dan Ross", phone: "(604) 892-8830", startDate: "2026-10-07", endDate: "2026-10-10", contract: r(48000), billed: r(48000), gate: "Underslab DWV Head Test, Radon Pipe & 15-Mil Stego Seal", status: "Completed", contractPdf: { name: "12_Underslab_Radon_Slab_Signed.pdf", date: "2026-10-01" }, docs: ["12_Underslab_Radon_Slab_Signed.pdf"], revisions: [] },
    { id: 13, phase: "13", name: "Structural Steel Moment Frames, W-Beams, HSS Columns & Crane Hoisting", sub: "Garibaldi Structural Steel Ltd", contact: "Shane Mercer", phone: "(604) 898-7741", startDate: "2026-10-11", endDate: "2026-10-14", contract: r(58000), billed: r(58000), gate: "CWB Weld Inspection & High-Strength Anchor Bolt Torque", status: "Completed", contractPdf: { name: "13_Structural_Steel_Subcontract_Signed.pdf", date: "2026-10-02" }, docs: ["13_Structural_Steel_Subcontract_Signed.pdf"], revisions: [] },
    { id: 14, phase: "14", name: "Rough Wood Framing, TJI Floor Joists, Shear Walls & #52603 Roof Trusses", sub: "Pacific Ridge Timberworks Ltd", contact: "Cody Lindstrom", phone: "(604) 815-4900", startDate: "2026-10-12", endDate: "2026-11-06", contract: r(245000), billed: r(140000), gate: "Structural P.Eng. Shearwall Nailing & Simpson ATS Review", status: "Active On-Site", contractPdf: { name: "14_Rough_Framing_Timberworks_Signed.pdf", date: "2026-10-02" }, docs: ["14_Rough_Framing_Timberworks_Signed.pdf", "Simpson_ATS_Shop_Drawings.pdf"], revisions: [] },
    { id: 15, phase: "15", name: "Standing Seam Metal Roofing, SBS Torch-On & Sheet Metal Flashing", sub: "Summit Architectural Sheet Metal", contact: "Brett Holloway", phone: "(604) 932-6610", startDate: "2026-11-09", endDate: "2026-11-21", contract: r(86000), billed: 0, gate: "RCABC / Building Envelope Roof Dry-In Inspection", status: "Scheduled", contractPdf: { name: "15_Summit_Roofing_SheetMetal_Signed.pdf", date: "2026-10-05" }, docs: ["15_Summit_Roofing_SheetMetal_Signed.pdf"], revisions: [] },
    { id: 16, phase: "16", name: "European Triple-Pane NAFS Windows, Skylights & Lift-Slide Doors", sub: "Innotech Windows & Doors BC", contact: "Lukas Weber", phone: "(604) 854-1122", startDate: "2026-11-02", endDate: "2026-11-14", contract: r(118000), billed: r(59000), gate: "NAFS/Step Code Window Sill Pan & SIGA Wigluv Flashing", status: "Active On-Site", contractPdf: { name: "16_Innotech_TriplePane_Glazing_Signed.pdf", date: "2026-09-18" }, docs: ["16_Innotech_TriplePane_Glazing_Signed.pdf"], revisions: [] },
    { id: 17, phase: "17", name: "Building Envelope, SIGA Air Barrier, Exterior Insulation & Rainscreen Cavity", sub: "Vantage Passive Wall Enclosure", contact: "Nils Lindqvist", phone: "(604) 738-9011", startDate: "2026-12-07", endDate: "2026-12-20", contract: r(92000), billed: r(40000), gate: "Envelope P.Eng. Continuous Exterior Insulation & WRB Review", status: "Scheduled", contractPdf: { name: "17_Vantage_Envelope_WRB_Signed.pdf", date: "2026-10-04" }, docs: ["17_Vantage_Envelope_WRB_Signed.pdf"], revisions: [
      
    ] },
    { id: 18, phase: "18", name: "BC Energy Step Code Mid-Build Blower Door Air-Tightness Test (<=1.0 ACH50)", sub: "E3 Eco Group Energy Advisors", contact: "Liam O'Connor, CEA", phone: "(604) 684-5588", startDate: "2026-12-21", endDate: "2026-12-23", contract: r(7500), billed: r(5000), gate: "Mid-Construction Air Tightness <= 1.0 ACH50 Verification", status: "Scheduled", contractPdf: { name: "18_E3_MidBuild_BlowerDoor_Signed.pdf", date: "2026-08-01" }, docs: ["18_E3_MidBuild_BlowerDoor_Signed.pdf"], revisions: [] },
    { id: 19, phase: "19", name: "Plumbing Rough-In, Domestic PEX-a, Natural Gas & Hydronic In-Floor", sub: "Pinnacle Mechanical & Plumbing", contact: "Dan Ross", phone: "(604) 892-8830", startDate: "2026-11-16", endDate: "2026-12-02", contract: r(94000), billed: r(28000), gate: "Municipal DWV & 100 PSI Hydronic Manifold Pressure Pass", status: "Active On-Site", contractPdf: { name: "19_Pinnacle_Plumbing_Hydronics_Signed.pdf", date: "2026-10-08" }, docs: ["19_Pinnacle_Plumbing_Hydronics_Signed.pdf"], revisions: [] },
    { id: 20, phase: "20", name: "Cold-Climate Heat Pumps & Zehnder ComfoAir HRV Balanced Ventilation", sub: "Coastline Hydronics & Air Quality", contact: "Evan Mercer", phone: "(604) 980-5519", startDate: "2026-11-23", endDate: "2026-12-09", contract: r(104000), billed: r(26000), gate: "Mechanical P.Eng Schedule B & TECA Ventilation Sign-Off", status: "Scheduled", contractPdf: { name: "20_Coastline_HVAC_Zehnder_Signed.pdf", date: "2026-10-10" }, docs: ["20_Coastline_HVAC_Zehnder_Signed.pdf"], revisions: [] },
    { id: 21, phase: "21", name: "Residential Fire Sprinkler System (NFPA 13D / 13R) & Hydrostatic Test", sub: "Sea-to-Sky Fire Protection Ltd", contact: "Kyle Barton", phone: "(604) 898-2090", startDate: "2026-11-30", endDate: "2026-12-08", contract: r(28000), billed: 0, gate: "200 PSI 2-Hour Hydrostatic Fire Suppression Test Pass", status: "Scheduled", contractPdf: { name: "21_Fire_Sprinkler_NFPA13R_Signed.pdf", date: "2026-10-11" }, docs: ["21_Fire_Sprinkler_NFPA13R_Signed.pdf"], revisions: [] },
    { id: 22, phase: "22", name: "Electrical 400A Primary Service, Rough-In, Low-Voltage & Dual EV Chargers", sub: "Current Energy Electrical Ltd", contact: "Ryan Chen, FSR", phone: "(604) 815-7733", startDate: "2026-12-01", endDate: "2026-12-18", contract: r(98000), billed: r(20000), gate: "Technical Safety BC Rough-In & EVEMS Load Management Pass", status: "Scheduled", contractPdf: { name: "22_Current_Electrical_400A_Signed.pdf", date: "2026-10-12" }, docs: ["22_Current_Electrical_400A_Signed.pdf"], revisions: [
      { id: "CO-003", date: "2026-10-14", title: "Add Second 80A Bidirectional EV Charger + LUTRON HomeWorks Scene Keypads", desc: "Owner requested upgrade to dual 80A bidirectional EV circuits in garage plus architectural Lutron lighting keypads in Great Room & Primary Suite.", amount: r(12400), days: 2, pdfName: "CO-003_Lutron_DualEV_Spec_Quote.pdf", signed: false, signedBy: "", signedDate: "" }
    ] },
    { id: 23, phase: "23", name: "Rockwool Thermal Insulation, STC 55+ Party-Wall Acoustic & Smart Vapor Retarder", sub: "Nordic Thermal Enclosures", contact: "Soren H.", phone: "(604) 987-3310", startDate: "2027-01-04", endDate: "2027-01-15", contract: r(54000), billed: 0, gate: "Municipal Insulation, Acoustic Channel & Smart Vapor Pass", status: "Scheduled", contractPdf: { name: "23_Nordic_Rockwool_Insulation_Signed.pdf", date: "2026-10-10" }, docs: ["23_Nordic_Rockwool_Insulation_Signed.pdf"], revisions: [] },
    { id: 24, phase: "24", name: "5/8\" Type X Fire-Rated Drywall Boarding, Resilient Channels & Level 5 Finish", sub: "Apex Drywall & Acoustic Finishing", contact: "Carlos Mendez", phone: "(604) 722-6190", startDate: "2027-01-18", endDate: "2027-02-05", contract: r(72000), billed: 0, gate: "1-Hour Fire Separation & Level 5 Skim Coat Moisture Check", status: "Scheduled", contractPdf: { name: "24_Apex_Drywall_Level5_Signed.pdf", date: "2026-10-12" }, docs: ["24_Apex_Drywall_Level5_Signed.pdf"], revisions: [] },
    { id: 25, phase: "25", name: "Architectural Fibre-Cement, Clear Western Red Cedar & Ventilated Soffits", sub: "Westcoast Rainscreen Cladding Ltd", contact: "Julian Dubois", phone: "(604) 738-9011", startDate: "2027-01-11", endDate: "2027-02-02", contract: r(66000), billed: 0, gate: "Building Envelope P.Eng 3/4\" Rainscreen & Bug-Screen Sign-Off", status: "Scheduled", contractPdf: { name: "25_Westcoast_Cedar_Cladding_Signed.pdf", date: "2026-10-12" }, docs: ["25_Westcoast_Cedar_Cladding_Signed.pdf"], revisions: [] },
    { id: 26, phase: "26", name: "Solid-Core Interior Doors, Reveal Baseboards, Casing & Timber/Steel Stairs", sub: "Squamish Fine Finishing Carpentry", contact: "Antoine Mercier", phone: "(604) 892-7120", startDate: "2027-02-08", endDate: "2027-02-20", contract: r(48000), billed: 0, gate: "BCBC Guardrail Geometry & Architectural Reveal Tolerance", status: "Scheduled", contractPdf: { name: "26_Fine_Finishing_Carpentry_Signed.pdf", date: "2026-10-12" }, docs: ["26_Fine_Finishing_Carpentry_Signed.pdf"], revisions: [] },
    { id: 27, phase: "27", name: "Custom European Millwork, Kitchen Cabinetry & Bookmatched Quartz Countertops", sub: "West Coast Architectural Woodwork & Surfaces", contact: "Henrik Lind", phone: "(604) 731-8800", startDate: "2027-02-15", endDate: "2027-03-04", contract: r(110000), billed: 0, gate: "Laser-Templated Waterfall Quartz & Blum Hardware QA", status: "Scheduled", contractPdf: { name: "27_WestCoast_Millwork_Quartz_Signed.pdf", date: "2026-10-14" }, docs: ["27_WestCoast_Millwork_Quartz_Signed.pdf"], revisions: [] },
    { id: 28, phase: "28", name: "Schluter Kerdi Waterproofing, Large-Format Porcelain Tile & White Oak Flooring", sub: "Artisan Tile & Hardwood Surfaces", contact: "Henrik Lind", phone: "(604) 731-8800", startDate: "2027-02-22", endDate: "2027-03-12", contract: r(75000), billed: 0, gate: "24-Hour Wet-Area Flood Test & Radiant Subfloor Moisture Check", status: "Scheduled", contractPdf: { name: "28_Artisan_Tile_WhiteOak_Signed.pdf", date: "2026-10-14" }, docs: ["28_Artisan_Tile_WhiteOak_Signed.pdf"], revisions: [] },
    { id: 29, phase: "29", name: "Architectural Zero-VOC Coatings, Starfire Glass Railings, Appliances & MEP Trims", sub: "Signature Coastal Painters & Glacier Glass", contact: "Andre Moreau", phone: "(604) 892-9940", startDate: "2027-03-08", endDate: "2027-03-20", contract: r(42000), billed: 0, gate: "Structural Glass Guardrail Cert, Electrical Final & HRV Balance", status: "Scheduled", contractPdf: { name: "29_Signature_Paint_Glass_Trim_Signed.pdf", date: "2026-10-14" }, docs: ["29_Signature_Paint_Glass_Trim_Signed.pdf"], revisions: [] },
    { id: 30, phase: "30", name: "Civil Permeable Paving, Alpine Landscaping, Final Blower Door, C-A/C-B & Occupancy", sub: "Keystone Possibilities Ltd. Finish Team (#52603)", contact: "Wayne Stevenson (#52603)", phone: "(604) 848-9688", startDate: "2027-03-21", endDate: "2027-03-31", contract: r(64000), billed: 0, gate: "Final Blower Door <=1.0 ACH50, Schedules C-A/C-B & Occupancy Permit", status: "Scheduled", contractPdf: { name: "30_Keystone_Final_Occupancy_Signed.pdf", date: "2026-10-14" }, docs: ["30_Keystone_Final_Occupancy_Signed.pdf"], revisions: [] }
  ];
}

function buildFactoryInspectionsForJob(municipality) {
  const muni = municipality || "District of Squamish";
  return [
    { id: "INSP-01", stage: "01", title: "Geotechnical Excavation & Competent Bedrock Bearing Review", authority: "Thurber Geotechnical P.Eng. (Schedule B)", date: "2026-08-24", status: "Passed", notes: "Competent granodiorite bedrock verified at 150 kPa+ allowable bearing pressure. Rock dowels approved.", pdfName: "INSP-01_Thurber_Bedrock_Bearing_Report.pdf" },
    { id: "INSP-02", stage: "02", title: "Footing Formwork, 15M/20M Rebar & Grounding Electrode Pre-Pour", authority: muni + " Building Inspector & Structural P.Eng.", date: "2026-09-18", status: "Passed", notes: "Footing rebar cages, 75mm clear cover chairs, and Ufer ground verified prior to concrete placement.", pdfName: "INSP-02_Footing_Rebar_PrePour_Pass.pdf" },
    { id: "INSP-03", stage: "03", title: "Foundation Stem Wall Rebar, Anchor Bolts & Simpson ATS Hold-Downs", authority: "Apex Structural Engineering (Schedule B)", date: "2026-09-22", status: "Passed", notes: "400mm grade beams, 20M longitudinal bars, and Simpson ATS anchor templates signed off.", pdfName: "INSP-03_StemWall_ATS_Anchors_Pass.pdf" },
    { id: "INSP-04", stage: "04", title: "Dampproofing, Dimple Membrane, 4\" Weeping Tile & 3/4\" Drain Rock", authority: muni + " Building Official", date: "2026-10-06", status: "Passed", notes: "Perimeter perforated PVC drain tile with filter sock and 12\" washed 3/4\" crush cover verified.", pdfName: "INSP-04_DrainTile_Backfill_Clearance.pdf" },
    { id: "INSP-05", stage: "05", title: "Underslab Plumbing DWV, Radon Rough-In, XPS Insulation & 15-Mil Poly", authority: muni + " Plumbing Inspector", date: "2026-10-09", status: "Passed", notes: "DWV head test passed, radon sub-slab depressurization rock & pipe sealed, Stego 15-mil vapor barrier intact.", pdfName: "INSP-05_Underslab_Plumbing_Radon_Pass.pdf" },
    { id: "INSP-06", stage: "06", title: "BCLS Foundation Siting & Top-of-Wall Elevation Survey Certificate", authority: "Sea-to-Sky Geomatics (BCLS)", date: "2026-10-12", status: "Passed", notes: "Setbacks and FCL elevation 144.50m certified compliant with approved building permit.", pdfName: "INSP-06_BCLS_Foundation_Survey_Cert.pdf" },
    { id: "INSP-07", stage: "07", title: "Structural Sheathing, Nailing Patterns, LVL Beams & Simpson ATS Torque", authority: "Apex Structural P.Eng. & " + muni, date: "2026-10-29", status: "Scheduled", notes: "Inspect 1/2\" CDX shear walls (8d @ 3\" O.C. edge) and continuous tie-down rod tensioning.", pdfName: "INSP-07_Framing_Shear_Checklist.pdf" },
    { id: "INSP-08", stage: "08", title: "Rough-In Plumbing, Hydronics, HVAC Ventilation & Electrical (TSBC)", authority: muni + " & Technical Safety BC", date: "2026-12-10", status: "Scheduled", notes: "Full MEP rough-in pressure tests, TECA HRV ducting, and TSBC 400A electrical clearance.", pdfName: "INSP-08_MEP_RoughIn_Protocol.pdf" },
    { id: "INSP-09", stage: "09", title: "Mid-Construction BC Energy Step Code 4 Blower Door Air Tightness Test", authority: "E3 Eco Group Certified Energy Advisor", date: "2026-12-22", status: "Scheduled", notes: "Target <= 1.0 ACH50 pressurized & depressurized air barrier verification prior to insulation.", pdfName: "INSP-09_MidBuild_BlowerDoor_Spec.pdf" },
    { id: "INSP-10", stage: "10", title: "Exterior Rainscreen Cavity, Window Flashing & Interior Rockwool Insulation", authority: "Building Envelope P.Eng. & " + muni, date: "2027-01-14", status: "Scheduled", notes: "Verify R-22 cavity + R-10 exterior continuous wood fiber and smart vapor barrier continuity.", pdfName: "INSP-10_Envelope_Insulation_Spec.pdf" },
    { id: "INSP-11", stage: "11", title: "Final Step Code As-Built Energy Compliance & HRV Balancing Report", authority: "E3 Eco Group & TECA Commissioning", date: "2027-03-18", status: "Scheduled", notes: "Final blower door test certificate and Zehnder ComfoAir room-by-room CFM balancing.", pdfName: "INSP-11_Final_StepCode_Compliance.pdf" },
    { id: "INSP-12", stage: "12", title: "Final Municipal Building Inspection, Letters of Assurance Schedule C-B & Occupancy", authority: muni + " Chief Building Official", date: "2027-03-29", status: "Scheduled", notes: "All Schedule C-A & C-B letters submitted; final life-safety, handrail, and occupancy sign-off.", pdfName: "INSP-12_Final_Occupancy_Permit_Package.pdf" }
  ];
}

function buildFactoryWalkthroughForJob() {
  return [
    { id: 1, area: "01. Foundation & Site Drainage", item: "Perimeter storm sumps, cleanouts, driveway slopes & architectural concrete finish verified", done: true },
    { id: 2, area: "02. Exterior Cladding & Rainscreen", item: "Clear cedar rainscreen joints, bug screens, flashings & standing seam roof terminations", done: true },
    { id: 3, area: "03. Windows & Exterior Doors", item: "Innotech triple-pane tilt-and-turn hardware operation, compression seals & screens", done: true },
    { id: 4, area: "04. Garage, 400A Panel & EV", item: "Circuit directory labeled, dual Level 2 EV chargers tested, overhead door sensors verified", done: false },
    { id: 5, area: "05. Mechanical & Zehnder HRV", item: "Heat pump zones, HRV filter access demonstrated to Owner, domestic hot water recirculation", done: false },
    { id: 6, area: "06. Chef's Kitchen & Cabinetry", item: "Rift-sawn white oak doors aligned, Blum soft-close drawers, quartz waterfall miters & appliances", done: false },
    { id: 7, area: "07. Great Room & White Oak Floors", item: "Engineered white oak plank transitions, flush vents, Level 5 drywall under raking light", done: false },
    { id: 8, area: "08. Primary Suite & Ensuite Bath", item: "Curbless shower flood test, heated tile floor thermostat, freestanding tub & vanity lighting", done: false },
    { id: 9, area: "09. Secondary Bedrooms & Baths", item: "Door latches, closet millwork, GFI outlets, exhaust interlocks & plumbing fixture flow", done: false },
    { id: 10, area: "10. Stairs, Glass Guards & Decks", item: "Solid timber floating treads, 1/2\" tempered glass guardrails, roof terrace membrane & drains", done: false },
    { id: 11, area: "11. Life Safety & Sprinklers", item: "NFPA 13D/13R concealed sprinkler escutcheons, interconnected smoke/COstrobes tested", done: false },
    { id: 12, area: "12. Keys, Manuals & 2-5-10 Binder", item: "All fobs/keys handed over, appliance warranties & 2-5-10 National Home Warranty activated", done: false }
  ];
}

function buildFactoryMaterialStagesForJob(scale) {
  const s = scale || 1.0;
  const q = (n) => Math.max(1, Math.round(n * s));
  return [
    {
      stageNum: 1,
      phase: "Stage 1: Site Prep, Land Clearing, Tree/Silt Fencing & Temp Site Setup",
      slips: [ { name: "Stage1_Site_Fencing_Erosion_Ticket.pdf", desc: "Perimeter fencing, silt barrier & temp power pole", date: "Jul 08, 2026" } ],
      items: [
        { desc: "6ft Galvanized Modular Construction Security Fencing Panels + Bases", uom: "LF", qty: q(280), waste: "0%", unit: 14.50, supplier: "Sea-to-Sky Site Rentals" },
        { desc: "Heavy-Duty Woven Geotextile Silt Fence with Treated Stakes (SPEA Buffer)", uom: "LF", qty: q(220), waste: "10%", unit: 6.80, supplier: "Squamish Building Supply" },
        { desc: "High-Visibility Orange Tree Protection Barrier Mesh + 2x4 Framing", uom: "Rolls", qty: q(6), waste: "5%", unit: 145.00, supplier: "Squamish Building Supply" },
        { desc: "Quarry Spall 3\"–6\" Stabilized Construction Entrance Tracking Pad Rock", uom: "Tons", qty: q(45), waste: "8%", unit: 38.00, supplier: "Coast Aggregates" }
      ]
    },
    {
      stageNum: 2,
      phase: "Stage 2: Excavation, Trenching, Geotextile, 3/4\" Drain Rock & Weeping Tile",
      slips: [ { name: "Stage2_Coast_Aggregates_DrainRock_Tickets.pdf", desc: "Washed 3/4\" clear crush & structural fill tickets", date: "Aug 28, 2026" } ],
      items: [
        { desc: "Non-Woven Separation Geotextile Filter Fabric (Mirafi 140N / 15ft Wide)", uom: "Rolls", qty: q(4), waste: "10%", unit: 490.00, supplier: "Convoy Supply" },
        { desc: "3/4\" Clear Washed Crushed Drain Rock (Perimeter & Underslab Capillary Break)", uom: "Tons", qty: q(135), waste: "8%", unit: 44.00, supplier: "Coast Aggregates" },
        { desc: "3/4\" Minus Structural Road Base Aggregate (Compacted in 6\" Lifts)", uom: "Tons", qty: q(110), waste: "8%", unit: 39.00, supplier: "Coast Aggregates" },
        { desc: "4\" Perforated PVC SDR-35 Foundation Weeping Tile + Filter Sock + Cleanouts", uom: "LF", qty: q(240), waste: "10%", unit: 12.50, supplier: "Emco Waterworks" },
        { desc: "4\" Solid PVC Storm Leader Collector Pipe & Fittings", uom: "LF", qty: q(210), waste: "8%", unit: 14.00, supplier: "Emco Waterworks" }
      ]
    },
    {
      stageNum: 3,
      phase: "Stage 3: Footings, Foundation Formwork, 15M/20M Rebar, 35 MPa Concrete & Dampproofing",
      slips: [
        { name: "Stage3_Burnco_35MPa_Batch_Tickets.pdf", desc: "35 MPa concrete pour batch tickets & slump logs", date: "Sep 24, 2026" },
        { name: "Stage3_Harris_Rebar_Mill_Certs.pdf", desc: "Grade 400W 15M & 20M deformed steel rebar", date: "Sep 12, 2026" }
      ],
      items: [
        { desc: "3/4\" High-Density Overlaid (HDO) Formply Foundation Panels (4x8)", uom: "Sheets", qty: q(145), waste: "10%", unit: 84.00, supplier: "Squamish Valley Timber" },
        { desc: "2x4 & 2x6 SPF Form Framing, Strongbacks, Walers & Snap-Ties/Wedges", uom: "Pkg", qty: 1, waste: "10%", unit: q(8400), supplier: "Squamish Valley Timber" },
        { desc: "15M & 20M Grade 400W Deformed Steel Reinforcing Rebar + 10M Stirrups", uom: "Tons", qty: q(12), waste: "6%", unit: 1850.00, supplier: "Harris Rebar" },
        { desc: "35 MPa Sulfate-Resistant Ready-Mix Concrete (Footings, Stem Walls & Slab)", uom: "m³", qty: q(148), waste: "6%", unit: 325.00, supplier: "Burnco Rock Products" },
        { desc: "Delta-MS Dimple Foundation Drainage Membrane + Termination Bar", uom: "Rolls", qty: q(9), waste: "8%", unit: 265.00, supplier: "Convoy Supply" },
        { desc: "15-Mil Stego Wrap Underslab Vapor Barrier + 2\" High-Density XPS Rigid Foam", uom: "SF", qty: q(1850), waste: "10%", unit: 3.85, supplier: "Convoy Supply" }
      ]
    },
    {
      stageNum: 4,
      phase: "Stage 4: Subfloor Framing (PT Sill Plates, PSL/LVL Beams, TJI Joists, Rim Board & 3/4\" Subfloor)",
      slips: [ { name: "Stage4_Weyerhaeuser_TJI_Subfloor_BOL.pdf", desc: "11-7/8\" TJI joists, PSL beams & Edge-Gold subfloor", date: "Oct 10, 2026" } ],
      items: [
        { desc: "2x6 Pressure-Treated Hem-Fir Mudsill Plates + 5.5\" Foam Sill Gasket Rolls", uom: "LF", qty: q(380), waste: "10%", unit: 4.40, supplier: "Squamish Valley Timber" },
        { desc: "Parallam PSL / 1-3/4\" Microllam LVL Structural Drop Beams & Posts", uom: "LF", qty: q(260), waste: "5%", unit: 28.50, supplier: "Weyerhaeuser / SVI" },
        { desc: "11-7/8\" Weyerhaeuser TJI 230/360 Engineered I-Joists (@ 16\" O.C.)", uom: "LF", qty: q(2850), waste: "6%", unit: 11.80, supplier: "Weyerhaeuser / SVI" },
        { desc: "1-1/4\" x 11-7/8\" TimberStrand LSL Structural Rim Board", uom: "LF", qty: q(420), waste: "8%", unit: 9.60, supplier: "Weyerhaeuser / SVI" },
        { desc: "3/4\" (23/32\") T&G Weyerhaeuser Edge-Gold OSB Subfloor Sheathing (4x8)", uom: "Sheets", qty: q(116), waste: "8%", unit: 62.00, supplier: "Squamish Valley Timber" },
        { desc: "LePage PL400 Heavy-Duty Subfloor Construction Adhesive (28oz Cartridges)", uom: "Tubes", qty: q(72), waste: "5%", unit: 13.50, supplier: "Squamish Building Supply" }
      ]
    },
    {
      stageNum: 5,
      phase: "Stage 5: Wall Framing Package (2x6 Exterior Studs, 2x4 Interior Studs, Plates, Kings/Jacks & LVL Headers)",
      slips: [ { name: "Stage5_KD_SPF_WallFraming_Lumber_Pack.pdf", desc: "2x6 & 2x4 KD SPF #2&Btr precision end-trimmed studs & plates", date: "Oct 14, 2026" } ],
      items: [
        { desc: "2x6 x 104-5/8\" (9ft Wall) KD SPF #2&Btr Precision Exterior Wall Studs", uom: "Pcs", qty: q(780), waste: "12%", unit: 11.40, supplier: "Squamish Valley Timber" },
        { desc: "2x6 KD SPF 12' & 16' Lengths (Bottom Plate + Double Top Plates + Cripples)", uom: "LF", qty: q(2250), waste: "10%", unit: 1.95, supplier: "Squamish Valley Timber" },
        { desc: "2x4 x 104-5/8\" (9ft Wall) KD SPF #2&Btr Interior Partition Wall Studs", uom: "Pcs", qty: q(890), waste: "10%", unit: 7.60, supplier: "Squamish Valley Timber" },
        { desc: "2x4 KD SPF 12' & 16' Lengths (Interior Bottom + Double Top Plates)", uom: "LF", qty: q(2780), waste: "10%", unit: 1.35, supplier: "Squamish Valley Timber" },
        { desc: "1-3/4\" x 9-1/2\" & 11-7/8\" 2.0E Microllam LVL Window & Door Headers", uom: "LF", qty: q(340), waste: "8%", unit: 18.90, supplier: "Weyerhaeuser / SVI" },
        { desc: "1/2\" 4-Ply Douglas Fir CDX Structural Shear Wall Sheathing (4x8 Sheets)", uom: "Sheets", qty: q(215), waste: "10%", unit: 48.50, supplier: "Squamish Valley Timber" },
        { desc: "2x6 & 2x8 Solid Wood Blocking (Kitchen Cabinets, TV Mounts, Bath Grab Bars)", uom: "LF", qty: q(480), waste: "10%", unit: 2.15, supplier: "Squamish Valley Timber" }
      ]
    },
    {
      stageNum: 6,
      phase: "Stage 6: Roof Framing (Engineered Roof Trusses, Valley Rafters, Fascia & 5/8\" CDX Roof Sheathing)",
      slips: [],
      items: [
        { desc: "Custom Engineered Wood Roof Trusses & Girder Trusses (Alpine Snow Load Stamped)", uom: "Pkg", qty: 1, waste: "0%", unit: q(34500), supplier: "Pacific Truss BC" },
        { desc: "2x10 & 2x12 KD Fir Valley Rafters, Outlookers, Barge Rafters & Ridge Blocking", uom: "LF", qty: q(640), waste: "10%", unit: 4.85, supplier: "Squamish Valley Timber" },
        { desc: "5/8\" 5-Ply Douglas Fir CDX Roof Deck Sheathing (4x8 Sheets) + H-Clips", uom: "Sheets", qty: q(82), waste: "10%", unit: 58.00, supplier: "Squamish Valley Timber" },
        { desc: "1x8 & 2x8 Primed Clear Fascia Trim Boards & Soffit Backing", uom: "LF", qty: q(340), waste: "8%", unit: 5.20, supplier: "Squamish Valley Timber" }
      ]
    },
    {
      stageNum: 7,
      phase: "Stage 7: Structural Hardware, Simpson Strong-Tie Hold-Downs/ATS Rods, Hangers & Fasteners",
      slips: [ { name: "Stage7_Simpson_StrongTie_Holdown_Schedule.pdf", desc: "Simpson ATS continuous rods, HDU8 holdowns & IUS hangers", date: "Oct 12, 2026" } ],
      items: [
        { desc: "1/2\" x 10\" Hot-Dip Galvanized Sill Anchor Bolts + 3\"x3\"x1/4\" Seismic Plate Washers", uom: "Pcs", qty: q(110), waste: "5%", unit: 9.80, supplier: "Simpson Strong-Tie / Fastenal" },
        { desc: "Simpson Strong-Tie Continuous ATS Tie-Down Rods, Couplers & Take-Up Devices", uom: "Sets", qty: q(16), waste: "0%", unit: 940.00, supplier: "Simpson Strong-Tie Canada" },
        { desc: "Simpson Strong-Tie HDU5 / HDU8 Pre-Deflected Shear Wall Hold-Downs + SDS Screws", uom: "Pcs", qty: q(24), waste: "0%", unit: 118.00, supplier: "Simpson Strong-Tie Canada" },
        { desc: "Simpson Strong-Tie IUS / LUS Top-Flange & Face-Mount TJI Joist Hangers", uom: "Pcs", qty: q(310), waste: "5%", unit: 6.40, supplier: "Squamish Building Supply" },
        { desc: "Paslode 3-1/4\" x .131\" Framing Nails + 2-3/8\" x .113\" Ring-Shank Shear Wall Nails", uom: "Cases", qty: q(18), waste: "5%", unit: 165.00, supplier: "Squamish Building Supply" }
      ]
    },
    {
      stageNum: 8,
      phase: "Stage 8: Building Envelope, Breathable Air Barrier, Exterior Insulation, Rainscreen Strapping & Decking",
      slips: [],
      items: [
        { desc: "SIGA Majvest 200 Breathable Weather/Air Barrier Membrane + Wigluv Sealing Tapes", uom: "Rolls", qty: q(14), waste: "8%", unit: 410.00, supplier: "475 High Performance Building" },
        { desc: "60mm Gutex Multitherm / Rockwool Comfortboard 80 Continuous Exterior Insulation", uom: "SF", qty: q(4400), waste: "8%", unit: 3.45, supplier: "475 High Performance Building" },
        { desc: "1x4 Pressure-Treated Plywood Vertical & Cross-Cavity Rainscreen Strapping + Bug Screen", uom: "LF", qty: q(3800), waste: "10%", unit: 1.45, supplier: "Squamish Valley Timber" },
        { desc: "8\" Structural Long-Wood Screws (Fastening Rainscreen Through Exterior Insulation)", uom: "Boxes", qty: q(16), waste: "5%", unit: 245.00, supplier: "475 High Performance Building" },
        { desc: "Architectural Clear Western Red Cedar Siding & Soffit Cladding Package", uom: "SF", qty: q(3200), waste: "10%", unit: 14.80, supplier: "Silva Timber Products" }
      ]
    }
  ];
}

function createJobPortalRecord(cfg) {
  const scale = cfg.scale || 1.0;
  const basePrice = cfg.contractPrice || 1850000;
  return {
    jobId: cfg.jobId,
    address: cfg.address,
    title: cfg.title,
    municipality: cfg.municipality,
    pid: cfg.pid || "014-882-192",
    permitNum: cfg.permitNum || "BP2026-0419",
    ownerName: cfg.ownerName,
    ownerPhone: cfg.ownerPhone,
    ownerEmail: cfg.ownerEmail,
    ownerPasscode: cfg.ownerPasscode,
    contractPrice: basePrice,
    scopeSummary: cfg.scopeSummary || "Complete turnkey construction under CCDC 5B / Fixed-Fee Construction Management including rock excavation, 35 MPa concrete foundations, engineered timber framing, BC Energy Step Code 4 enclosure, and 2-5-10 National Home Warranty coverage.",
    whereWeAreDate: cfg.whereWeAreDate || "2026-10-15",
    whereWeAreStage: cfg.whereWeAreStage || "Stage 09: Rough Wood Framing, TJI Floor Joists & Roof Trusses",
    whereWeArePct: cfg.whereWeArePct || 48,
    contractPdf: {
      name: cfg.contractPdfName || ("CCDC5B_Executed_Prime_Contract_" + cfg.jobId + ".pdf"),
      date: cfg.contractDate || "Jul 02, 2026",
      size: "4.2 MB",
      dataUrl: ""
    },
    builderSig: {
      name: "Wayne Stevenson",
      title: "President & Licensed Builder #52603 — Keystone Possibilities Ltd.",
      date: "Jul 02, 2026"
    },
    ownerSig: {
      signed: true,
      typedName: cfg.ownerName,
      date: "Jul 02, 2026",
      dataUrl: ""
    },
    warranty: {
      provider: "National Home Warranty / WBI Home Warranty Insurance",
      builderLicense: "BC Housing Licensed Builder #52603 (Keystone Possibilities Ltd.)",
      policyNum: cfg.warrantyPolicy || "NHW-2026-88421",
      status: "Enrolled & Active — 2-5-10 Statutory Protection",
      commencement: "Upon Municipal Occupancy Permit",
      pdfName: "National_Home_Warranty_2-5-10_Certificate_" + cfg.jobId + ".pdf",
      pdfDataUrl: ""
    },
    planSets: {
      arch: {
        discipline: "📐 Architect Plans (AIBC Issued for Construction Set)",
        firm: "Studio Vance Architecture AIBC",
        rev: "Rev 3 (IFC) — Sheets A-101 to A-401",
        date: "Aug 15, 2026",
        pdfName: cfg.jobId + "_Architect_AIBC_Full_Plans_IFC.pdf",
        dataUrl: ""
      },
      eng: {
        discipline: "⚙️ Engineer Plans (Structural P.Eng., Simpson ATS & Geotech)",
        firm: "Apex Structural P.Eng. & Thurber Geotechnical",
        rev: "Rev 3 (Sealed Schedule B) — Sheets S-101 to E-101",
        date: "Aug 18, 2026",
        pdfName: cfg.jobId + "_Structural_Geotech_Engineering_Sealed.pdf",
        dataUrl: ""
      },
      city: {
        discipline: "🏛️ City Approved Plans & Stamped Building Permit Set",
        firm: cfg.municipality + " Building & Civil Dept",
        rev: "Permit #" + (cfg.permitNum || "BP2026-0419") + " Municipal Red-Stamp Set",
        date: "Aug 22, 2026",
        pdfName: cfg.jobId + "_City_Approved_Stamped_Permit_Plans.pdf",
        dataUrl: ""
      }
    },
    takeoffParams: {
      footprintSf: cfg.footprintSf || 1600,
      storeys: cfg.storeys || 2,
      extWallLf: cfg.extWallLf || 340,
      intWallLf: cfg.intWallLf || 420,
      wallHeight: 9,
      studSpacing: 16,
      openings: 26,
      fndLf: cfg.fndLf || 180,
      fndHeight: 8,
      roofPitch: 1.12,
      planPdfName: cfg.jobId + "_Framing_Takeoff_Blueprint_Set.pdf",
      planPdfDataUrl: ""
    },
    draws: [
      { id: "D-01", stage: "Draw 1: Deposit, Mobilization, Permitting & Geotech Setup", pct: 10, status: "Paid", pdfName: "Draw01_Paid_Receipt.pdf" },
      { id: "D-02", stage: "Draw 2: Rock Excavation, Civil ES54 & 35 MPa Concrete Foundation Complete", pct: 20, status: "Paid", pdfName: "Draw02_Foundation_Paid_Receipt.pdf" },
      { id: "D-03", stage: "Draw 3: Structural Framing, Roof Dry-In & Simpson ATS Engineer Sign-Off", pct: 25, status: "Due Now", pdfName: "Draw03_Framing_Progress_Invoice.pdf" },
      { id: "D-04", stage: "Draw 4: Triple-Pane Windows, MEP Rough-In & Mid-Build Blower Door Pass", pct: 20, status: "Scheduled", pdfName: "" },
      { id: "D-05", stage: "Draw 5: Exterior Rainscreen, Drywall Level 5, Millwork & White Oak Flooring", pct: 15, status: "Scheduled", pdfName: "" },
      { id: "D-06", stage: "Draw 6: Final Municipal Occupancy Permit & Pre-Occupancy Walkthrough", pct: 10, status: "Scheduled", pdfName: "" }
    ],
    vaultDocs: [
      { title: "CCDC_5B_Executed_Prime_Contract_" + cfg.jobId + ".pdf", desc: "Signed by Wayne Stevenson (#52603) & " + cfg.ownerName, date: "Jul 02, 2026" },
      { title: "BC_Builders_Lien_Act_Sec5_10Pct_Trust_Schedule.pdf", desc: "Statutory 10% Holdback Escrow Protocol", date: "Jul 02, 2026" },
      { title: "National_Home_Warranty_2-5-10_Policy_" + (cfg.warrantyPolicy || "NHW-2026-88421") + ".pdf", desc: "2-Yr Materials, 5-Yr Envelope, 10-Yr Structural", date: "Jul 10, 2026" },
      { title: cfg.municipality.replace(/\s+/g, "_") + "_Building_Permit_" + (cfg.permitNum || "BP2026-0419") + ".pdf", desc: "Municipal Stamped Permit Approval", date: "Aug 22, 2026" }
    ],
    contacts: [
      { id: 1, role: "Prime Builder & Superintendent", name: "Wayne Stevenson", license: "BC Housing Licensed Builder #52603", phone: "(604) 848-9688", email: "wayne@keystonepossibilities.ca" },
      { id: 2, role: "Registered Property Owner(s)", name: cfg.ownerName, license: "PID: " + (cfg.pid || "014-882-192"), phone: cfg.ownerPhone, email: cfg.ownerEmail },
      { id: 3, role: "Architect of Record", name: "Marcus Vance, Architect AIBC", license: "Studio Vance Architecture AIBC", phone: "(604) 732-8812", email: "m.vance@studiovance.ca" },
      { id: 4, role: "Structural Engineer (Schedule B)", name: "Apex Structural Engineering", license: "EGBC Permit #100482", phone: "(604) 688-9920", email: "projects@apexstructural.bc.ca" },
      { id: 5, role: "Geotechnical Engineer (Schedule B)", name: "Dr. Arthur Tremblay, P.Eng.", license: "Thurber Geotechnical Ltd.", phone: "(604) 984-4321", email: "a.tremblay@thurber.ca" },
      { id: 6, role: "Municipal Building Official", name: cfg.municipality + " Building Dept", license: "Permit #" + (cfg.permitNum || "BP2026-0419"), phone: "(604) 892-5217", email: "building@squamish.ca" }
    ],
    trades: buildFactoryTradesForJob(scale, 0),
    inspections: buildFactoryInspectionsForJob(cfg.municipality),
    walkthrough: buildFactoryWalkthroughForJob(),
    walkthroughSigned: false,
    walkthroughSignedDate: "",
    walkthroughPdfName: cfg.jobId + "_PreOccupancy_Walkthrough_Checklist.pdf",
    materials: buildFactoryMaterialStagesForJob(scale),
    calendarLogs: {
      "2026-10-15": {
        notes: "Framing crew installing Level 2 Weyerhaeuser 11-7/8\" TJI joists and 3/4\" Edge-Gold T&G subfloor. Simpson Strong-Tie ATS continuous rod couplers inspected on gridlines A–D. Lumber moisture verified at 12.4%.",
        checkpoints: [
          { text: "Verify Simpson ATS rod coupler witness holes prior to sheathing", done: true },
          { text: "Subfloor glued with PL400 & ring-shank nailed @ 6\" edge / 12\" field", done: true },
          { text: "Confirm triple-pane window rough opening laser dimensions", done: true }
        ],
        trades: ["Rough Wood Framing", "Structural Steel"],
        photos: [ { name: "Oct15_TJI_Subfloor_Deck.pdf", desc: "Level 2 floor deck & ATS rods verified" } ]
      }
    }
  };
}

const FACTORY_JOBS_LIST = [
  createJobPortalRecord({
    jobId: "KP-2026-001",
    address: "40484 Tantalus Rd, Squamish, BC",
    title: "Highland Luxury Mountain Multiplex",
    municipality: "District of Squamish",
    pid: "014-882-192",
    permitNum: "BP2026-0419",
    ownerName: "David & Sarah Kensington",
    ownerPhone: "(604) 555-8821",
    ownerEmail: "kensington.squamish@gmail.com",
    ownerPasscode: "",
    contractPrice: 1850000,
    scale: 1.0,
    footprintSf: 1600,
    storeys: 2,
    extWallLf: 340,
    intWallLf: 420,
    fndLf: 180,
    whereWeAreDate: "2026-10-15",
    whereWeAreStage: "Stage 09: Rough Wood Framing, TJI Floor Joists & Roof Trusses",
    whereWeArePct: 48,
    warrantyPolicy: "NHW-2026-88421"
  }),
  createJobPortalRecord({
    jobId: "KP-2026-002",
    address: "1428 Chartwell Dr, West Vancouver, BC",
    title: "Chartwell Oceanview Architectural Concrete Residence",
    municipality: "District of West Vancouver",
    pid: "009-441-810",
    permitNum: "BP-WV-2026-118",
    ownerName: "Marcus & Elena Sterling",
    ownerPhone: "(604) 922-7410",
    ownerEmail: "m.sterling@sterlingcapital.ca",
    ownerPasscode: "",
    contractPrice: 4250000,
    scale: 2.1,
    footprintSf: 2650,
    storeys: 3,
    extWallLf: 480,
    intWallLf: 640,
    fndLf: 240,
    whereWeAreDate: "2026-10-15",
    whereWeAreStage: "Stage 06: 35 MPa Board-Formed Concrete Foundation & Suspended Slab",
    whereWeArePct: 32,
    warrantyPolicy: "NHW-2026-91044"
  }),
  createJobPortalRecord({
    jobId: "KP-2026-003",
    address: "7124 Nancy Greene Dr, Whistler, BC",
    title: "Fitzsimmons Alpine Heavy Timber & Stone Chalet",
    municipality: "Resort Municipality of Whistler (RMOW)",
    pid: "021-773-905",
    permitNum: "RMOW-BP-2026-309",
    ownerName: "Harrison Vance Holdings Ltd.",
    ownerPhone: "(604) 938-4190",
    ownerEmail: "hvance@vanceholdings.com",
    ownerPasscode: "",
    contractPrice: 3480000,
    scale: 1.75,
    footprintSf: 2200,
    storeys: 2,
    extWallLf: 410,
    intWallLf: 520,
    fndLf: 210,
    whereWeAreDate: "2026-10-15",
    whereWeAreStage: "Stage 10: European Triple-Pane Glazing & Heavy Timber Roof Dry-In",
    whereWeArePct: 56,
    warrantyPolicy: "NHW-2026-94310"
  })
];

// ============================================================================
// 2. MULTI-JOB STATE ENGINE & PERSISTENCE
// ============================================================================
const LS_MULTI_KEY = "KEYSTONE_PORTAL_V14_SINGLE_JOB_MASTER";
let portalStore = loadMultiJobStore();

function loadMultiJobStore() {
  try {
    const raw = localStorage.getItem(LS_MULTI_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && Array.isArray(parsed.jobs) && parsed.jobs.length > 0) {
        return parsed;
      }
    }
  } catch (e) {
    console.warn("Portal store load fallback:", e);
  }
  return {
    activeJobId: "KP-2026-001",
    jobs: JSON.parse(JSON.stringify(FACTORY_JOBS_LIST))
  };
}

function getActiveJob() {
  let job = portalStore.jobs.find(j => j.jobId === portalStore.activeJobId);
  if (!job) {
    job = portalStore.jobs[0];
    portalStore.activeJobId = job.jobId;
  }
  return job;
}

function saveState(silent) {
  try {
    localStorage.setItem(LS_MULTI_KEY, JSON.stringify(portalStore));
  } catch (e) {
    console.warn("Could not save to localStorage:", e);
  }
  clearTimeout(window.__kpAutoSyncTimer);
  window.__kpAutoSyncTimer = setTimeout(() => {
    try { syncAllJobsToServerAndHub(true); } catch (err) {}
  }, 450);
}

function escapeHtml(str) {
  return String(str == null ? "" : str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmtMoney(n) {
  const val = Number(n) || 0;
  const sign = val < 0 ? "-" : "";
  return sign + "$" + Math.abs(Math.round(val)).toLocaleString("en-CA");
}

function showToast(msg) {
  const t = document.getElementById("kp-toast");
  if (!t) return;
  t.innerText = msg;
  t.style.display = "block";
  clearTimeout(window.__kpToastTimer);
  window.__kpToastTimer = setTimeout(() => { t.style.display = "none"; }, 3400);
}

// ============================================================================
// 3. LOGIN GATE, JOB SWITCHER & NEW JOB PORTAL CREATION
// ============================================================================
function renderJobSelectors() {
  const loginSel = document.getElementById("ks-job-select");
  const hdrSel = document.getElementById("kp-header-job-select");
  const activeJob = getActiveJob();

  if (loginSel) {
    loginSel.innerHTML = portalStore.jobs.map(j =>
      `<option value="${escapeHtml(j.jobId)}" ${j.jobId === activeJob.jobId ? "selected" : ""}>${escapeHtml(j.address)} (${escapeHtml(j.jobId)})</option>`
    ).join("");
  }
  if (hdrSel) {
    hdrSel.innerHTML = portalStore.jobs.map(j =>
      `<option value="${escapeHtml(j.jobId)}" ${j.jobId === activeJob.jobId ? "selected" : ""}>${escapeHtml(j.address)} (${escapeHtml(j.jobId)})</option>`
    ).join("");
  }
  const clientInput = document.getElementById("ks-client-id");
  if (clientInput && activeJob && !clientInput.value) clientInput.value = activeJob.address;
}

function onLoginJobSelectChange(jobId) {
  portalStore.activeJobId = jobId;
  saveState(true);
  const j = getActiveJob();
  const clientInput = document.getElementById("ks-client-id");
  if (clientInput && j) clientInput.value = j.address;
  const demoBtnAddr = document.getElementById("ks-demo-btn-addr");
  if (demoBtnAddr && j) demoBtnAddr.innerText = j.address;
}

function getBuilderAuthHeaders() {
  const headers = { "Content-Type": "application/json" };
  let tok = window.kpBuilderSessionToken || "";
  if (!tok) {
    try { tok = sessionStorage.getItem("KP_BUILDER_SESSION_TOKEN") || ""; } catch (e) {}
  }
  if (tok) {
    headers["X-KP-Builder-Session"] = tok;
    headers["X-KP-Portal-Session"] = tok;
  }
  const wpNonce = (window.kpPortalConfig && window.kpPortalConfig.nonce) || (window.keystoneData && window.keystoneData.nonce) || (window.wpApiSettings && window.wpApiSettings.nonce) || "";
  if (wpNonce) {
    headers["X-WP-Nonce"] = wpNonce;
  }
  return headers;
}

async function handlePortalLogin() {
  const selId = (document.getElementById("ks-job-select") || {}).value || "KP-2026-001";
  const typed = ((document.getElementById("ks-client-id") || {}).value || "").trim().toLowerCase();
  const rawPass = ((document.getElementById("ks-passcode") || {}).value || "").trim();
  const pass = rawPass.toLowerCase();
  const errEl = document.getElementById("ks-auth-error");
  const submitBtn = document.getElementById("btn-submit-login");

  if (!rawPass) {
    if (errEl) errEl.style.display = "block";
    return;
  }

  let matchedJob = portalStore.jobs.find(j =>
    j.jobId.toLowerCase() === typed ||
    j.address.toLowerCase().includes(typed) ||
    j.ownerName.toLowerCase().includes(typed)
  );
  if (!matchedJob) {
    matchedJob = portalStore.jobs.find(j => j.jobId === selId) || getActiveJob();
  }
  const targetJobId = matchedJob ? matchedJob.jobId : (selId || "KP-2026-001");
  const authEndpoint = (window.kpPortalConfig && window.kpPortalConfig.authUrl) || "/wp-json/keystone/v1/portal-auth";

  if (submitBtn) submitBtn.disabled = true;

  let unlocked = false;
  let authEndpointReachable = false;

  try {
    const resp = await fetch(authEndpoint, {
      method: "POST",
      headers: getBuilderAuthHeaders(),
      body: JSON.stringify({
        jobId: targetJobId,
        job_id: targetJobId,
        passcode: rawPass
      })
    });

    if (resp.status !== 404) {
      authEndpointReachable = true;
    }

    if (resp.ok) {
      const data = await resp.json();
      if (data && (data.ok || data.success || data.authenticated || data.sessionToken || data.token || data.session_token || data.builder_session)) {
        const sessionToken = data.sessionToken || data.token || data.session_token || data.builder_session || "";
        if (sessionToken) {
          window.kpBuilderSessionToken = sessionToken;
          try { sessionStorage.setItem("KP_BUILDER_SESSION_TOKEN", sessionToken); } catch (e) {}
        }
        if (data.job && typeof data.job === "object") {
          const jid = data.job.jobId || data.job.job_id || data.job.id || targetJobId;
          data.job.jobId = jid;
          const idx = portalStore.jobs.findIndex(j => j.jobId === jid);
          if (idx >= 0) {
            portalStore.jobs[idx] = Object.assign({}, portalStore.jobs[idx], data.job);
            matchedJob = portalStore.jobs[idx];
          } else {
            portalStore.jobs.push(data.job);
            matchedJob = data.job;
          }
        }
        unlocked = true;
      }
    } else if (resp.status === 429 && errEl) {
      try {
        const rateErr = await resp.json();
        if (rateErr && rateErr.message) errEl.textContent = rateErr.message;
      } catch (e) {}
    }
  } catch (e) {
    authEndpointReachable = false;
  } finally {
    if (submitBtn) submitBtn.disabled = false;
  }

  // Graceful fallback ONLY if WP admin session already hydrated non-empty job passcode via /portal-jobs
  if (!unlocked && !authEndpointReachable && matchedJob) {
    const adminHydratedPass = String(matchedJob.ownerPasscode || matchedJob.builderPasscode || "").trim().toLowerCase();
    if (adminHydratedPass && pass === adminHydratedPass) {
      unlocked = true;
    }
  }

  if (unlocked && matchedJob) {
    if (errEl) errEl.style.display = "none";
    portalStore.activeJobId = matchedJob.jobId;
    saveState(true);
    launchDemoProject();
    showToast("Unlocked Job Portal: " + matchedJob.address);
  } else {
    if (errEl) errEl.style.display = "block";
  }
}

function launchDemoProject() {
  const loginCard = document.getElementById("ks-login-card");
  const authPortal = document.getElementById("ks-authenticated-portal");
  if (loginCard) loginCard.style.display = "none";
  if (authPortal) {
    authPortal.style.setProperty("display", "block", "important");
  }
  renderAllPortalComponents();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function lockPortalSession() {
  const loginCard = document.getElementById("ks-login-card");
  const authPortal = document.getElementById("ks-authenticated-portal");
  if (authPortal) authPortal.style.setProperty("display", "none", "important");
  if (loginCard) loginCard.style.display = "block";
  window.kpBuilderSessionToken = "";
  try { sessionStorage.removeItem("KP_BUILDER_SESSION_TOKEN"); } catch (e) {}
  const passEl = document.getElementById("ks-passcode");
  if (passEl) passEl.value = "";
  renderJobSelectors();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function switchActiveJob(jobId) {
  portalStore.activeJobId = jobId;
  saveState();
  renderAllPortalComponents();
  const j = getActiveJob();
  showToast("📍 Switched Active Job Portal to: " + j.address);
}

function openCreateJobFromGate() {
  launchDemoProject();
  openNewJobModal();
}

function openNewJobModal() {
  openModal("modal-new-job");
}

function createNewJobPortalFromModal() {
  const addr = (document.getElementById("nj-address").value || "").trim();
  if (!addr) {
    alert("Please enter the Job Civic Address.");
    return;
  }
  const title = (document.getElementById("nj-title").value || "").trim() || ("Custom Residence & Build — " + addr);
  const muni = (document.getElementById("nj-municipality").value || "").trim() || "District of Squamish";
  const ownerName = (document.getElementById("nj-owner-name").value || "").trim() || "Property Owner";
  const ownerPhone = (document.getElementById("nj-owner-phone").value || "").trim() || "(604) 555-0199";
  const price = Number(document.getElementById("nj-contract-price").value) || 2150000;
  const pass = (document.getElementById("nj-passcode").value || "").trim() || "";
  const startDate = document.getElementById("nj-start-date").value || "2026-11-02";
  const footprint = Number(document.getElementById("nj-footprint").value) || 1650;

  const nextNum = portalStore.jobs.length + 1;
  const newJobId = "KP-2026-00" + nextNum;
  const scale = Math.max(0.6, Math.round((price / 1850000) * 100) / 100);

  const newJob = createJobPortalRecord({
    jobId: newJobId,
    address: addr,
    title: title,
    municipality: muni,
    pid: "018-990-" + (100 + nextNum),
    permitNum: "BP2026-0" + (500 + nextNum),
    ownerName: ownerName,
    ownerPhone: ownerPhone,
    ownerEmail: "owner@" + addr.split(" ")[1].toLowerCase().replace(/[^a-z0-9]/g, "") + ".ca",
    ownerPasscode: pass,
    contractPrice: price,
    scale: scale,
    footprintSf: footprint,
    storeys: 2,
    extWallLf: Math.round(Math.sqrt(footprint) * 4 * 1.15),
    intWallLf: Math.round(footprint * 0.26),
    fndLf: Math.round(Math.sqrt(footprint) * 4),
    whereWeAreDate: startDate,
    whereWeAreStage: "Stage 01: Land Survey, BCLS Pinning & Pre-Construction Mobilization",
    whereWeArePct: 8,
    warrantyPolicy: "NHW-2026-99" + (100 + nextNum)
  });

  portalStore.jobs.push(newJob);
  portalStore.activeJobId = newJob.jobId;
  saveState();
  closeModal("modal-new-job");
  renderAllPortalComponents();
  syncAllJobsToServerAndHub(true);
  showToast("✨ Created & Activated New Job Portal: " + addr);
}

// ============================================================================
// 4. NAVIGATION & MODAL HELPERS
// ============================================================================
let activePage = 1;

function switchPortalPage(pageNum, btn) {
  activePage = pageNum;
  document.querySelectorAll(".kp-pane").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".kp-nav-tab").forEach(t => {
    if (Number(t.getAttribute("data-tab")) === Number(pageNum)) t.classList.add("active");
    else t.classList.remove("active");
  });
  const targetPane = document.getElementById("kp-page-" + pageNum);
  if (targetPane) targetPane.classList.add("active");
  if (btn) btn.classList.add("active");

  if (pageNum === 2) {
    renderCalendar();
    renderActiveTradeRadar();
  }
  if (pageNum === 3) {
    renderWarrantyAndPlansTab();
    renderActiveBlueprint();
  }
  if (pageNum === 5) {
    calculateSmartTakeoff();
    renderMaterialsList();
  }
  if (pageNum === 6) {
    renderTab6JobManager();
  }
  if (pageNum === 7 && typeof renderTab7ThirtyStagesAndGeotech === "function") {
    renderTab7ThirtyStagesAndGeotech();
  }
}

function openModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.add("open");
    m.style.display = "flex";
  }
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.remove("open");
    m.style.display = "none";
  }
}

window.addEventListener("click", (e) => {
  if (e.target && e.target.classList && e.target.classList.contains("kp-modal-backdrop")) {
    e.target.classList.remove("open");
    e.target.style.display = "none";
  }
});

window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document.querySelectorAll(".kp-modal-backdrop").forEach(m => {
      m.classList.remove("open");
      m.style.display = "none";
    });
  }
});

function triggerDummyDownload(filename, titleOrContent, dataUrl) {
  if (dataUrl && dataUrl.startsWith("data:")) {
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    return;
  }
  const job = getActiveJob();
  const lines = [
    "JOB ADDRESS: " + job.address + " (" + job.jobId + ")",
    "PROJECT TITLE: " + job.title + " | MUNICIPALITY: " + resolveJobMunicipality(job),
    "BUILDING PERMIT: #" + job.permitNum,
    "PROPERTY OWNER(S): " + job.ownerName + " | " + job.ownerPhone,
    "PRIME BUILDER: Keystone Possibilities Ltd. - Wayne Stevenson (BC #52603)",
    "DOCUMENT FILE: " + filename,
    "GENERATED: " + new Date().toLocaleString(),
    "------------------------------------------------------------------------"
  ].concat(String(titleOrContent || "Official verified project PDF record.").split(/\r?\n/));
  const blob = buildRealPdfBinaryBlob(filename, job.address + " (" + job.jobId + ")", lines);
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

// ============================================================================
// 5. TAB 1: OWNER & CONTRACT (Contract Price, PDF Vault, Signature Pad, Revisions & Draws)
// ============================================================================
function getJobSignedRevisionsSum(job) {
  let signedSum = 0;
  let signedCount = 0;
  let pendingCount = 0;
  (job.trades || []).forEach(t => {
    (t.revisions || []).forEach(rev => {
      if (rev.signed) {
        signedSum += Number(rev.amount) || 0;
        signedCount++;
      } else {
        pendingCount++;
      }
    });
  });
  return { signedSum, signedCount, pendingCount };
}


// ============================================================================
// REAL BINARY %PDF-1.4 GENERATOR, DYNAMIC DISTRICT/PERMIT & INTERACTIVE DAY PREVIEW
// ============================================================================
function resolveJobMunicipality(job) {
  if (job.municipality && String(job.municipality).trim()) {
    const m = String(job.municipality).trim();
    const addr = String(job.address || "").toLowerCase();
    // Auto-match jurisdiction if address city changed
    if (addr.includes("vancouver") && !addr.includes("north") && !addr.includes("west") && m.includes("Squamish")) return "City of Vancouver";
    if (addr.includes("north vancouver") && m.includes("Squamish")) return "District of North Vancouver";
    if (addr.includes("west vancouver") && m.includes("Squamish")) return "District of West Vancouver";
    if (addr.includes("whistler") && m.includes("Squamish")) return "Resort Municipality of Whistler";
    if (addr.includes("burnaby") && m.includes("Squamish")) return "City of Burnaby";
    if (addr.includes("coquitlam") && m.includes("Squamish")) return "City of Coquitlam";
    return m;
  }
  const addr = String(job.address || "").toLowerCase();
  if (addr.includes("squamish")) return "District of Squamish";
  if (addr.includes("whistler")) return "Resort Municipality of Whistler";
  if (addr.includes("north vancouver")) return "District of North Vancouver";
  if (addr.includes("west vancouver")) return "District of West Vancouver";
  if (addr.includes("vancouver")) return "City of Vancouver";
  if (addr.includes("burnaby")) return "City of Burnaby";
  return "District of Squamish";
}

function promptEditMunicipalityAndPermit() {
  const job = getActiveJob();
  const curMuni = resolveJobMunicipality(job);
  const newMuni = prompt("Enter Municipal / City Jurisdiction for this project:", curMuni);
  if (newMuni === null) return;
  const newPermit = prompt("Enter City / Municipal Building Permit Number:", job.permitNum || "BP2026-0419");
  if (newPermit === null) return;
  job.municipality = newMuni.trim() || curMuni;
  job.permitNum = newPermit.trim().replace(/^#/, "") || job.permitNum;
  savePortalState();
  renderTab1Contract();
  showToast("Updated Jurisdiction (" + job.municipality + ") & Permit #" + job.permitNum);
}

let selectedTab1PreviewDay = 15; // Defaults to Today (Oct 15, 2026)

function getOctoberDayWriteUp(job, dayNum) {
  const dateStr = "2026-10-" + String(dayNum).padStart(2, "0");
  const dows = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  // Oct 1, 2026 is Thursday (index 4)
  const dowName = dows[(dayNum + 3) % 7];
  const isWeekend = ((dayNum + 3) % 7 === 0) || ((dayNum + 3) % 7 === 6);

  // Check if a custom note was saved in job.dayLogs
  const customLog = (job.dayLogs && job.dayLogs[dateStr] && job.dayLogs[dateStr].notes) ? String(job.dayLogs[dateStr].notes).trim() : "";

  const presetWriteUps = {
    1: {
      stage: "Stage 07 — Dampproofing & Foundation Envelope",
      crew: "Pacific Envelope & Waterproofing",
      status: "Completed",
      summary: "Applied 2-coat elastomeric foundation membrane and dimple drainage mat across North & East foundation walls. Perimeter drain tile bedded in washed 3/4\" clear crush."
    },
    2: {
      stage: "Stage 07 — Foundation Drain Tile & Backfill Prep",
      crew: "Pacific Envelope & Tantalus Civil",
      status: "Completed",
      summary: "Completed weeping tile cleanouts, filter cloth wrap, and District of Squamish pre-backfill drainage inspection sign-off (#BP2026-0419)."
    },
    5: {
      stage: "Stage 08 — Structural Steel Columns & Moment Frames",
      crew: "Cascade Structural Steel Ltd.",
      status: "Completed",
      summary: "Mobile crane on site at 7:30 AM. Set W12x65 wide-flange steel beams and HSS 6x6 posts on main level anchor bolts; torqued high-strength bolts to P.Eng. spec."
    },
    6: {
      stage: "Stage 08 — Structural Steel Welding & Decking",
      crew: "Cascade Structural Steel Ltd.",
      status: "Completed",
      summary: "CWB certified field welding on garage portal moment frame and cantilevered deck outriggers. Applied zinc-rich primer to all field welds."
    },
    7: {
      stage: "Stage 08 — Structural Steel P.Eng. Field Review",
      crew: "Apex Structural P.Eng. & Cascade Steel",
      status: "Completed",
      summary: "Apex Structural P.Eng. completed Schedule B field inspection of all steel moment connections and base-plate grouting. Zero deficiencies noted."
    },
    8: {
      stage: "Stage 08 — Sill Plates & Perimeter Anchor Verification",
      crew: "Pacific Ridge Timberworks Ltd.",
      status: "Completed",
      summary: "Installed pressure-treated 2x6 mudsills with Sill Seal acoustic/air barrier gasket; torqued 5/8\" galvanized anchor washers ahead of framing package arrival."
    },
    9: {
      stage: "Stage 08 — Engineered Lumber & TJI Joist Delivery",
      crew: "Pacific Ridge Timberworks Ltd.",
      status: "Completed",
      summary: "Received flat-deck delivery of Weyerhaeuser TJI 360 floor joists, 1-3/4\" Microllam LVL beams, and kiln-dried Douglas Fir framing package; staged and tarped on site."
    },
    12: {
      stage: "Stage 09 — Main Level 2x6 Exterior Shearwalls",
      crew: "Pacific Ridge Timberworks Ltd. (6 Carpenters)",
      status: "Completed",
      summary: "Commenced Stage 09 Rough Wood Framing. Framed and plumbed North and West 2x6 exterior bearing walls (16\" O.C.) and installed 1/2\" Douglas Fir plywood shear panels."
    },
    13: {
      stage: "Stage 09 — Main Level Interior Partitions & LVL Headers",
      crew: "Pacific Ridge Timberworks Ltd. (6 Carpenters)",
      status: "Completed",
      summary: "Set double and triple 1-3/4\" x 11-7/8\" LVL window headers across living room view glazing wall; framed acoustic party-wall double stud assemblies."
    },
    14: {
      stage: "Stage 09 — Level 2 TJI Floor System & Rim Board",
      crew: "Pacific Ridge Timberworks Ltd. (6 Carpenters)",
      status: "Completed Yesterday",
      summary: "Installed Level 2 TJI 360 floor joists at 16\" O.C. into Simpson strong-tie hangers, glued & ring-shank nailed 3/4\" Advantech T&G subfloordecking, and strapped shear transfers."
    },
    15: {
      stage: "Stage 09 — Level 2 Exterior Walls & Glulam Ridge Prep (TODAY)",
      crew: "Pacific Ridge Timberworks Ltd. (7 Carpenters On Site)",
      status: "Active Today (48% Stage Complete)",
      summary: "Standing Level 2 exterior 2x6 walls and setting Simpson HDU8 hold-downs tied to foundation rods. Crane boom scheduled 2:30 PM to hoist main Glulam ridge beams to Level 2 deck."
    },
    16: {
      stage: "Stage 09 — Level 2 Shearwall Sheathing & Glulam Posts",
      crew: "Pacific Ridge Timberworks Ltd. (7 Carpenters)",
      status: "Scheduled Tomorrow",
      summary: "Complete Level 2 exterior plywood shearwall nailing (4\" edge / 12\" field per S-201 schedule) and set custom Douglas Fir Glulam posts for upper mountain-view roof canopy."
    },
    17: {
      stage: "Stage 09 — Weekend Site Security & Weather Protection",
      crew: "Keystone Site Supervision",
      status: "Scheduled",
      summary: "Material inventory check, temporary bracing inspection, and subfloor water-shedding sweep ahead of Monday roof truss crane mobilization."
    },
    19: {
      stage: "Stage 09 — Engineered Roof Truss Crane Hoisting",
      crew: "Pacific Ridge Timberworks & Sea-to-Sky Crane",
      status: "Upcoming",
      summary: "45-ton mobile crane scheduled on site to hoist prefabricated engineered roof trusses onto Level 2 bearing walls; install permanent lateral truss bracing."
    },
    20: {
      stage: "Stage 09 — Roof Truss Bracing & Hurricane Ties",
      crew: "Pacific Ridge Timberworks Ltd.",
      status: "Upcoming",
      summary: "Install Simpson H2.5A hurricane ties at every truss bearing point and frame custom dormer/overhang outlookers per Sheet A-201."
    }
  };

  let entry = presetWriteUps[dayNum];
  if (!entry) {
    if (dayNum < 12) {
      entry = {
        stage: "Stages 07–08 — Waterproofing & Structural Steel",
        crew: isWeekend ? "Weekend Site Standby" : "Cascade Structural Steel Ltd.",
        status: "Completed",
        summary: isWeekend
          ? "Weekend curing & site safety check. Perimeter fencing and erosion control (ES54) verified intact."
          : "Completed structural steel framing alignments, anchor bolt torque verification, and foundation perimeter prep ahead of timber framing mobilization."
      };
    } else {
      entry = {
        stage: "Stage 09 — Rough Wood Framing & Roof Trusses",
        crew: isWeekend ? "Weekend Site Security & Check" : "Pacific Ridge Timberworks Ltd.",
        status: dayNum < 15 ? "Completed" : "Scheduled in Stage 09",
        summary: isWeekend
          ? "Weekend site walk, lumber tarp securing, and moisture meter check on engineered wood framing."
          : "Continuing Stage 09 structural wood framing, 5/8\" roof sheathing installation, and preparation for Apex Structural P.Eng. Schedule B framing walkthrough."
      };
    }
  }

  return {
    dayNum,
    dateStr,
    dowName,
    labelDate: `${dowName}, Oct ${dayNum}, 2026`,
    stage: entry.stage,
    crew: entry.crew,
    status: entry.status,
    writeUp: customLog || entry.summary,
    isToday: dayNum === 15
  };
}

function selectMiniCalDay(dayNum) {
  selectedTab1PreviewDay = Number(dayNum) || 15;
  renderTab1Contract();
}

function promptEditDayWriteUpFromTab1(dayNum) {
  const job = getActiveJob();
  const info = getOctoberDayWriteUp(job, dayNum);
  const updated = prompt(`Update Daily Write-Up for ${info.labelDate}:`, info.writeUp);
  if (updated === null) return;
  if (!job.dayLogs) job.dayLogs = {};
  if (!job.dayLogs[info.dateStr]) {
    job.dayLogs[info.dateStr] = { notes: "", trades: [info.crew], checkpoints: [], photos: [] };
  }
  job.dayLogs[info.dateStr].notes = updated.trim();
  savePortalState();
  renderTab1Contract();
  showToast(`Saved Daily Write-Up for Oct ${dayNum}, 2026`);
}

function buildRealPdfBinaryBlob(title, subtitle, linesArray) {
  const cleanPdfText = (s) => String(s || "")
    .replace(/[^\x20-\x7E]/g, " ")
    .replace(/\\/g, "\\\\")
    .replace(/\(/g, "\\(")
    .replace(/\)/g, "\\)");

  const streamLines = [
    "BT",
    "/F1 14 Tf",
    "50 750 Td",
    "(" + cleanPdfText("KEYSTONE POSSIBILITIES LTD. - BC LICENSED BUILDER #52603") + ") Tj",
    "0 -20 Td",
    "/F1 12 Tf",
    "(" + cleanPdfText(title) + ") Tj",
    "0 -16 Td",
    "/F1 9 Tf",
    "(" + cleanPdfText(subtitle) + ") Tj",
    "0 -22 Td"
  ];

  (linesArray || []).slice(0, 38).forEach(line => {
    streamLines.push("(" + cleanPdfText(line).slice(0, 95) + ") Tj");
    streamLines.push("0 -15 Td");
  });
  streamLines.push("ET");
  const contentStream = streamLines.join("\n");

  const objects = [];
  objects.push("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n");
  objects.push("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n");
  objects.push("3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n");
  objects.push("4 0 obj\n<< /Length " + contentStream.length + " >>\nstream\n" + contentStream + "\nendstream\nendobj\n");
  objects.push("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n");

  let pdf = "%PDF-1.4\n";
  const offsets = [0];
  objects.forEach(obj => {
    offsets.push(pdf.length);
    pdf += obj;
  });
  const xrefStart = pdf.length;
  pdf += "xref\n0 " + (objects.length + 1) + "\n";
  pdf += "0000000000 65535 f \n";
  for (let i = 1; i <= objects.length; i++) {
    pdf += String(offsets[i]).padStart(10, "0") + " 00000 n \n";
  }
  pdf += "trailer\n<< /Size " + (objects.length + 1) + " /Root 1 0 R >>\nstartxref\n" + xrefStart + "\n%%EOF";
  return new Blob([pdf], { type: "application/pdf" });
}

let currentPdfViewerZoom = 1.0;
function zoomPdfViewerModal(delta) {
  currentPdfViewerZoom = Math.min(1.8, Math.max(0.65, Math.round((currentPdfViewerZoom + delta) * 100) / 100));
  const wrap = document.getElementById("kp-pdf-viewer-zoom-wrap");
  const lbl = document.getElementById("kp-pdf-zoom-label");
  if (wrap) wrap.style.transform = "scale(" + currentPdfViewerZoom + ")";
  if (lbl) lbl.innerText = Math.round(currentPdfViewerZoom * 100) + "%";
}

function getJobBacktrackedCapitalStats(job) {
  const revStats = getJobSignedRevisionsSum(job);
  const revisedTotal = (Number(job.contractPrice) || 0) + revStats.signedSum;
  let runningSpent = 0;
  let completedStagesCount = 0;
  let activeStageObj = null;

  (job.trades || []).forEach(tr => {
    const trRevSum = (tr.revisions || []).filter(r => r.signed).reduce((a, r) => a + (Number(r.amount) || 0), 0);
    const trSpent = (Number(tr.billed) || 0) + trRevSum;
    runningSpent += trSpent;
    if (tr.status === "Completed") completedStagesCount++;
    if (tr.status === "In Progress" && !activeStageObj) activeStageObj = tr;
  });

  const remainingCapital = Math.max(0, revisedTotal - runningSpent);
  const holdbackOnSpent = Math.round(runningSpent * 0.10);
  const totalHoldback = Math.round(revisedTotal * 0.10);
  const spentPct = revisedTotal > 0 ? Math.min(100, Math.round((runningSpent / revisedTotal) * 1000) / 10) : 0;

  return {
    revisedTotal,
    runningSpent,
    remainingCapital,
    spentPct,
    holdbackOnSpent,
    totalHoldback,
    completedStagesCount,
    activeStageObj
  };
}

function openMasterPdfOnScreen(docKey) {
  const job = getActiveJob();
  const muniName = resolveJobMunicipality(job);
  const cap = getJobBacktrackedCapitalStats(job);
  const revStats = getJobSignedRevisionsSum(job);
  const modal = document.getElementById("modal-pdf-viewer");
  const titleEl = document.getElementById("pdf-modal-title");
  const bodyEl = document.getElementById("pdf-modal-body");
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (!modal || !bodyEl) return;

  currentPdfViewerZoom = 1.0;

  if (docKey === "permit") {
    const permitFile = `${job.jobId}_Municipal_Building_Permit_${job.permitNum}.pdf`;
    if (titleEl) titleEl.innerText = "PDF Viewer — " + permitFile;
    if (dlBtn) {
      dlBtn.innerText = "Download Permit PDF";
      dlBtn.onclick = () => triggerDummyDownload(permitFile, "Official Municipal Building Permit #" + job.permitNum + " issued by " + muniName);
    }
    bodyEl.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; background:#0b0f17; border:1px solid rgba(212,175,55,0.4); border-radius:9999px; padding:7px 16px; margin:0 auto 16px auto; max-width:850px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="kp-badge-pill kp-badge-gold">ISSUED MUNICIPAL BUILDING PERMIT PDF</span>
          <span style="font-size:0.75rem; color:#e2e8f0; font-weight:700;">${escapeHtml(muniName)} &bull; Permit #${escapeHtml(job.permitNum)}</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button type="button" onclick="window.print()" class="kp-secondary-btn kp-pill-sm">Print PDF</button>
          <button type="button" onclick="triggerDummyDownload('${escapeHtml(permitFile)}', 'Municipal Building Permit #${escapeHtml(job.permitNum)}')" class="kp-gold-btn kp-pill-sm">Download PDF</button>
        </div>
      </div>
      <div class="kp-pdf-page-sheet">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
          <div>
            <div style="font-size:0.74rem; font-weight:800; letter-spacing:0.12em; color:#475569; text-transform:uppercase;">${escapeHtml(muniName)} &bull; Building &amp; Development Services</div>
            <h2 style="font-size:1.45rem; font-weight:900; color:#0f172a; margin:4px 0 2px 0; font-family:'Outfit','Plus Jakarta Sans',sans-serif;">ISSUED BUILDING PERMIT #${escapeHtml(job.permitNum)}</h2>
            <div style="font-size:0.84rem; font-weight:700; color:#1e293b;">Civic Address: ${escapeHtml(job.address)} (PID: ${escapeHtml(job.pid)})</div>
          </div>
          <div style="text-align:right;">
            <div style="background:#0f172a; color:#d4af37; font-weight:900; font-size:0.72rem; padding:5px 10px; border-radius:4px;">STATUS: ISSUED &amp; ACTIVE</div>
            <div style="font-size:0.74rem; color:#475569; margin-top:4px;">Builder: <strong>Keystone Possibilities Ltd. (#52603)</strong></div>
          </div>
        </div>
        <p style="font-size:0.84rem; line-height:1.65; color:#1e293b !important;">
          Permission is hereby granted by <strong>${escapeHtml(muniName)}</strong> to <strong>Keystone Possibilities Ltd. (Wayne Stevenson, BC Licensed Builder #52603)</strong> and Owner(s) <strong>${escapeHtml(job.ownerName)}</strong> to construct the approved project in accordance with the stamped Architectural Drawings (${escapeHtml(job.planSets && job.planSets.arch ? job.planSets.arch.firm : "Studio Vance Architecture AIBC")}) and Sealed Structural/Geotechnical Schedule B Engineering Drawings (${escapeHtml(job.planSets && job.planSets.eng ? job.planSets.eng.firm : "Apex Structural P.Eng.")}) filed under Permit <strong>#${escapeHtml(job.permitNum)}</strong>.
        </p>
      </div>
    `;
    modal.classList.add("open");
    modal.style.display = "flex";
    return;
  }

  if (docKey === "contract") {
    const filename = job.contractPdfName || ("CCDC5B_Executed_Prime_Contract_" + job.jobId + ".pdf");
    if (titleEl) titleEl.innerText = "PDF Viewer — " + filename;
    if (dlBtn) {
      dlBtn.innerText = "Download Contract PDF";
      dlBtn.onclick = () => downloadPrimaryContractPdf();
    }

    if (job.contractPdfDataUrl && job.contractPdfDataUrl.startsWith("data:application/pdf")) {
      bodyEl.innerHTML = `<iframe src="${job.contractPdfDataUrl}" style="width:100%; height:76vh; border:none; border-radius:6px; background:#fff;"></iframe>`;
      modal.classList.add("open");
      modal.style.display = "flex";
      return;
    }

    bodyEl.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; background:#0b0f17; border:1px solid rgba(212,175,55,0.4); border-radius:9999px; padding:7px 16px; margin:0 auto 16px auto; max-width:850px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="kp-badge-pill kp-badge-gold">CCDC 5B EXECUTED CONTRACT PDF</span>
          <span style="font-size:0.75rem; color:#e2e8f0; font-weight:700;">${escapeHtml(filename)} &bull; Pages 1–2</span>
        </div>
        <div style="display:flex; align-items:center; gap:6px;">
          <button type="button" onclick="zoomPdfViewerModal(-0.1)" class="kp-secondary-btn kp-pill-sm">&minus;</button>
          <span id="kp-pdf-zoom-label" style="font-size:0.74rem; font-weight:800; color:#ffffff; min-width:44px; text-align:center;">100%</span>
          <button type="button" onclick="zoomPdfViewerModal(0.1)" class="kp-secondary-btn kp-pill-sm">+</button>
          <button type="button" onclick="window.print()" class="kp-secondary-btn kp-pill-sm">Print PDF</button>
          <button type="button" onclick="downloadPrimaryContractPdf()" class="kp-gold-btn kp-pill-sm">Download PDF</button>
        </div>
      </div>

      <div id="kp-pdf-viewer-zoom-wrap" style="transform-origin:top center; transition:transform 0.18s ease;">
        <div class="kp-pdf-page-sheet">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
            <div>
              <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.12em; color:#475569; text-transform:uppercase;">Canadian Construction Documents Committee &bull; Standard Fixed-Fee / CCDC 5B</div>
              <h2 style="font-size:1.45rem; font-weight:900; color:#0f172a; margin:4px 0 2px 0; font-family:'Outfit','Plus Jakarta Sans',sans-serif;">PRIME RESIDENTIAL &amp; MULTIPLEX CONSTRUCTION AGREEMENT</h2>
              <div style="font-size:0.84rem; font-weight:700; color:#1e293b;">Project: ${escapeHtml(job.address)} (${escapeHtml(job.title)})</div>
            </div>
            <div style="text-align:right;">
              <div style="background:#0f172a; color:#d4af37; font-weight:900; font-size:0.72rem; padding:5px 10px; border-radius:4px; letter-spacing:0.06em;">BC LICENSED BUILDER #52603</div>
              <div style="font-size:0.74rem; color:#475569; margin-top:4px;">Jurisdiction: <strong>${escapeHtml(muniName)}</strong></div>
              <div style="font-size:0.74rem; color:#475569;">Building Permit: <strong>#${escapeHtml(job.permitNum)}</strong></div>
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:14px 16px;">
            <div>
              <div style="font-size:0.68rem; font-weight:800; text-transform:uppercase; color:#64748b; letter-spacing:0.06em;">ARTICLE A-1 &mdash; PRIME BUILDER</div>
              <div style="font-size:0.95rem; font-weight:900; color:#0f172a; margin-top:2px;">Keystone Possibilities Ltd.</div>
              <div style="font-size:0.78rem; color:#334155;">Superintendent: Wayne Stevenson (BC Housing #52603)</div>
              <div style="font-size:0.76rem; color:#475569;">Direct: (604) 848-9688 &bull; wayne@keystonepossibilities.ca</div>
            </div>
            <div>
              <div style="font-size:0.68rem; font-weight:800; text-transform:uppercase; color:#64748b; letter-spacing:0.06em;">ARTICLE A-2 &mdash; REGISTERED PROPERTY OWNER(S)</div>
              <div style="font-size:0.95rem; font-weight:900; color:#0f172a; margin-top:2px;">${escapeHtml(job.ownerName)}</div>
              <div style="font-size:0.78rem; color:#334155;">Civic Site: ${escapeHtml(job.address)} (PID: ${escapeHtml(job.pid)})</div>
              <div style="font-size:0.76rem; color:#475569;">Contact: ${escapeHtml(job.ownerPhone)} &bull; ${escapeHtml(job.ownerEmail)}</div>
            </div>
          </div>

          <div style="margin-bottom:18px;">
            <div style="font-size:0.74rem; font-weight:900; text-transform:uppercase; color:#0f172a; letter-spacing:0.06em; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:8px;">ARTICLE A-3 &mdash; SCOPE OF WORK &amp; BUILDING CODE STANDARD</div>
            <p style="font-size:0.82rem; line-height:1.6; color:#1e293b !important; margin:0;">
              ${escapeHtml(job.scopeSummary)} All work shall be executed in strict compliance with the British Columbia Building Code 2024, ${escapeHtml(muniName)} bylaws, Sealed Structural Engineering Schedule B drawings, and 2-5-10 National Home Warranty Policy #${escapeHtml(job.warrantyPolicy)}.
            </p>
          </div>

          <div style="margin-bottom:20px;">
            <div style="font-size:0.74rem; font-weight:900; text-transform:uppercase; color:#0f172a; letter-spacing:0.06em; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:8px;">ARTICLE A-4 &mdash; CONTRACT SUM, APPROVED REVISIONS &amp; RUNNING CAPITAL LEDGER</div>
            <table style="width:100%; border-collapse:collapse; font-size:0.8rem;">
              <thead>
                <tr style="background:#0f172a; color:#ffffff;">
                  <th style="padding:8px 10px; text-align:left;">Financial Schedule Item</th>
                  <th style="padding:8px 10px; text-align:left;">Statutory / CCDC Reference</th>
                  <th style="padding:8px 10px; text-align:right;">Amount (CAD)</th>
                </tr>
              </thead>
              <tbody>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:8px 10px; font-weight:700; color:#0f172a;">1. Executed Baseline Contract Price</td>
                  <td style="padding:8px 10px; color:#475569;">CCDC 5B Article A-4 Baseline Sum</td>
                  <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">${fmtMoney(job.contractPrice)}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:8px 10px; font-weight:700; color:#0f172a;">2. Approved &amp; Signed Change Orders (${revStats.signedCount} Signed)</td>
                  <td style="padding:8px 10px; color:#475569;">Owner-Approved Scope Revisions</td>
                  <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">+${fmtMoney(revStats.signedSum)}</td>
                </tr>
                <tr style="border-bottom:2px solid #0f172a; background:#fefce8;">
                  <td style="padding:9px 10px; font-weight:900; color:#0f172a;">3. Revised Total Project Contract Amount</td>
                  <td style="padding:9px 10px; font-weight:700; color:#0f172a;">Current Governing Contract Obligation</td>
                  <td style="padding:9px 10px; text-align:right; font-weight:900; font-size:0.95rem; color:#0f172a;">${fmtMoney(cap.revisedTotal)}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:8px 10px; font-weight:700; color:#0f172a;">4. Running Capital Spent to Date (Stages 01–09)</td>
                  <td style="padding:8px 10px; color:#475569;">Verified Cumulative Progress Spend (${cap.spentPct}%)</td>
                  <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">${fmtMoney(cap.runningSpent)}</td>
                </tr>
                <tr style="border-bottom:1px solid #e2e8f0;">
                  <td style="padding:8px 10px; font-weight:700; color:#0f172a;">5. Remaining Capital Balance to Completion</td>
                  <td style="padding:8px 10px; color:#475569;">Unbilled Stages 14–30 Balance</td>
                  <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">${fmtMoney(cap.remainingCapital)}</td>
                </tr>
                <tr>
                  <td style="padding:8px 10px; font-weight:700; color:#0f172a;">6. 10% Statutory Builders Lien Holdback</td>
                  <td style="padding:8px 10px; color:#475569;">BC Builders Lien Act (55-Day Trust Account)</td>
                  <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">${fmtMoney(cap.holdbackOnSpent)} (of ${fmtMoney(cap.totalHoldback)})</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:24px; padding-top:16px; border-top:2px solid #0f172a;">
            <div>
              <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">EXECUTED BY PRIME BUILDER</div>
              <div style="font-family:Georgia,serif; font-style:italic; font-size:1.35rem; font-weight:700; color:#0f172a; margin:6px 0 2px 0;">Wayne Stevenson</div>
              <div style="font-size:0.75rem; font-weight:700; color:#334155;">Wayne Stevenson &bull; Keystone Possibilities Ltd. (#52603)</div>
              <div style="font-size:0.72rem; color:#64748b;">Signed: ${escapeHtml(job.builderSigDate || "2026-07-02")}</div>
            </div>
            <div>
              <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">EXECUTED BY PROPERTY OWNER(S)</div>
              <div style="font-family:Georgia,serif; font-style:italic; font-size:1.35rem; font-weight:700; color:#0f172a; margin:6px 0 2px 0;">${escapeHtml(job.ownerSigName || job.ownerName)}</div>
              <div style="font-size:0.75rem; font-weight:700; color:#334155;">${escapeHtml(job.ownerName)}</div>
              <div style="font-size:0.72rem; color:#64748b;">Signed &amp; Verified on Record</div>
            </div>
          </div>
        </div>
      </div>
    `;
    modal.classList.add("open");
    modal.style.display = "flex";
    return;
  }

  // Architect ('arch') or Engineering ('eng') Master PDF Viewer
  const ps = (job.planSets && job.planSets[docKey]) ? job.planSets[docKey] : null;
  if (!ps) return;
  if (titleEl) titleEl.innerText = "PDF Blueprint Viewer — " + ps.pdfName;
  if (dlBtn) {
    dlBtn.innerText = "Download " + (docKey === "arch" ? "Architect" : "Engineering") + " PDF";
    dlBtn.onclick = () => downloadPlanSetPdf(docKey);
  }

  if (ps.pdfDataUrl && ps.pdfDataUrl.startsWith("data:application/pdf")) {
    bodyEl.innerHTML = `<iframe src="${ps.pdfDataUrl}" style="width:100%; height:76vh; border:none; border-radius:6px; background:#fff;"></iframe>`;
    modal.classList.add("open");
    modal.style.display = "flex";
    return;
  }

  const blueprintSvg = (typeof generateBlueprintSvg === "function") ? generateBlueprintSvg(docKey, job, ps) : "";
  bodyEl.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; background:#0b0f17; border:1px solid rgba(212,175,55,0.4); border-radius:9999px; padding:7px 16px; margin:0 auto 16px auto; max-width:1020px;">
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="kp-badge-pill kp-badge-gold">${docKey === "arch" ? "ARCHITECTURAL IFC PDF SET" : "STRUCTURAL & GEOTECH P.ENG. PDF SET"}</span>
        <span style="font-size:0.75rem; color:#e2e8f0; font-weight:700;">${escapeHtml(muniName)} &bull; Permit #${escapeHtml(job.permitNum)}</span>
      </div>
      <div style="display:flex; align-items:center; gap:6px;">
        <button type="button" onclick="zoomPdfViewerModal(-0.1)" class="kp-secondary-btn kp-pill-sm">&minus;</button>
        <span id="kp-pdf-zoom-label" style="font-size:0.74rem; font-weight:800; color:#ffffff; min-width:44px; text-align:center;">100%</span>
        <button type="button" onclick="zoomPdfViewerModal(0.1)" class="kp-secondary-btn kp-pill-sm">+</button>
        <button type="button" onclick="window.print()" class="kp-secondary-btn kp-pill-sm">Print PDF</button>
        <button type="button" onclick="downloadPlanSetPdf('${docKey}')" class="kp-gold-btn kp-pill-sm">Download PDF</button>
      </div>
    </div>

    <div id="kp-pdf-viewer-zoom-wrap" style="transform-origin:top center; transition:transform 0.18s ease;">
      <div class="kp-pdf-blueprint-sheet">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; border-bottom:1px solid rgba(212,175,55,0.35); padding-bottom:12px; margin-bottom:14px;">
          <div>
            <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.1rem; font-weight:900; color:#ffffff;">${escapeHtml(ps.title)}</div>
            <div style="font-size:0.76rem; color:#d4af37; font-weight:700;">Firm of Record: ${escapeHtml(ps.firm)} &bull; Lead: ${escapeHtml(ps.lead)}</div>
          </div>
          <div style="text-align:right; font-size:0.74rem; color:#cbd5e1;">
            <div>City / District: <strong style="color:#ffffff;">${escapeHtml(muniName)} (Permit #${escapeHtml(job.permitNum)})</strong></div>
            <div>Site: <strong style="color:#d4af37;">${escapeHtml(job.address)}</strong></div>
          </div>
        </div>

        <div style="background:#02060d; border:1px solid rgba(255,255,255,0.16); border-radius:6px; overflow:hidden; margin-bottom:16px;">
          ${blueprintSvg}
        </div>

        <div style="font-size:0.75rem; font-weight:900; text-transform:uppercase; color:#d4af37; letter-spacing:0.07em; margin-bottom:8px;">
          Included Sealed Drawing Sheets in ${escapeHtml(ps.pdfName)} (Filed Under Permit #${escapeHtml(job.permitNum)}):
        </div>
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:8px;">
          ${(ps.sheets || []).map(sh => `
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.12); border-radius:8px; padding:8px 12px; display:flex; justify-content:space-between; align-items:center; gap:8px;">
              <div>
                <span style="color:#d4af37; font-weight:900; font-size:0.78rem; margin-right:6px;">${escapeHtml(sh.num)}</span>
                <strong style="color:#ffffff; font-size:0.78rem;">${escapeHtml(sh.name)}</strong>
                <div style="font-size:0.7rem; color:#94a3b8; margin-top:2px;">${escapeHtml(sh.notes)}</div>
              </div>
              <span class="kp-badge-pill kp-badge-white">Scale ${escapeHtml(sh.scale)}</span>
            </div>
          `).join("")}
        </div>
      </div>
    </div>
  `;
  modal.classList.add("open");
  modal.style.display = "flex";
}

function renderTab1Contract() {
  const job = getActiveJob();
  const muniName = resolveJobMunicipality(job);
  const revStats = getJobSignedRevisionsSum(job);
  const cap = getJobBacktrackedCapitalStats(job);

  // 1. Update Locked Top Header Bar (Job Title + Owner Name)
  const hdrOwner = document.getElementById("kp-header-owner-name");
  if (hdrOwner) hdrOwner.innerText = job.ownerName;
  const staticTitle = document.getElementById("kp-header-static-job-title");
  if (staticTitle) staticTitle.innerText = job.address;
  const staticSub = document.getElementById("kp-header-static-job-sub");
  if (staticSub) staticSub.innerText = (job.title || "Custom Build") + " (" + job.jobId + ")";

  // 2. Section 1: Project Amount & Backtracked Running Capital Spent + Dynamic District & Permit
  const idBadge = document.getElementById("p1-job-id-badge");
  if (idBadge) idBadge.innerText = job.jobId;
  const muniBadge = document.getElementById("p1-municipality-badge");
  if (muniBadge) muniBadge.innerText = muniName + " • Permit #" + job.permitNum;
  const addrTitle = document.getElementById("p1-job-address-title");
  if (addrTitle) addrTitle.innerText = job.address + " — Project Amount & Running Capital";

  const elBase = document.getElementById("p1-kpi-base-price");
  if (elBase) elBase.innerText = fmtMoney(job.contractPrice);
  const elRevSum = document.getElementById("p1-kpi-revisions-sum");
  if (elRevSum) elRevSum.innerText = (revStats.signedSum >= 0 ? "+" : "") + fmtMoney(revStats.signedSum);
  const elRevTotal = document.getElementById("p1-kpi-revised-total");
  if (elRevTotal) elRevTotal.innerText = fmtMoney(cap.revisedTotal);

  const elSpent = document.getElementById("p1-kpi-running-spent");
  if (elSpent) elSpent.innerText = fmtMoney(cap.runningSpent);
  const elSpentSub = document.getElementById("p1-kpi-running-spent-sub");
  const activePhaseNum = cap.activeStageObj ? cap.activeStageObj.phase : "09";
  if (elSpentSub) elSpentSub.innerText = `${cap.spentPct}% of Project Spent • Backtracked Stages 01–${activePhaseNum}`;

  const elRem = document.getElementById("p1-kpi-remaining-capital");
  if (elRem) elRem.innerText = fmtMoney(cap.remainingCapital);
  const elRemSub = document.getElementById("p1-kpi-remaining-sub");
  if (elRemSub) elRemSub.innerText = `${(100 - cap.spentPct).toFixed(1)}% Remaining Capital to Completion`;

  const elHold = document.getElementById("p1-kpi-holdback");
  if (elHold) elHold.innerText = fmtMoney(cap.holdbackOnSpent);
  const elHoldSub = document.getElementById("p1-kpi-holdback-sub");
  if (elHoldSub) elHoldSub.innerText = `Retained on Spend (${fmtMoney(cap.totalHoldback)} Total Contract Holdback)`;

  // 3. Section 2: Where We Are Sitting (Left: Completion + Selected Day Write-Up Preview | Right: Interactive October Calendar)
  const dayInfo = getOctoberDayWriteUp(job, selectedTab1PreviewDay);
  const tlDate = document.getElementById("p1-timeline-date-badge");
  if (tlDate) {
    tlDate.innerText = dayInfo.isToday
      ? "Previewing Today: Oct 15, 2026 • Click Any Date on Calendar to Preview"
      : `Previewing Selected Date: ${dayInfo.labelDate}`;
  }

  const activeStagePanel = document.getElementById("p1-active-stage-summary-panel");
  if (activeStagePanel) {
    const st = cap.activeStageObj || (job.trades && job.trades[8]) || {
      phase: "09",
      name: "Rough Wood Framing, TJI Floor Joists & Roof Trusses",
      sub: "Pacific Ridge Timberworks Ltd",
      start: "2026-10-12",
      end: "2026-11-06",
      contract: 245000,
      billed: 140000
    };
    const pct = Math.min(100, Math.max(5, Number(job.whereWeArePct) || 48));

    activeStagePanel.innerHTML = `
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:5px;">
          <span class="kp-badge-pill kp-badge-gold">ACTIVE ON SITE &bull; STAGE ${escapeHtml(st.phase)} OF 30</span>
          <span style="font-size:0.78rem; font-weight:900; color:#d4af37;">${pct}% Stage Complete</span>
        </div>
        <h3 style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.02rem; font-weight:900; color:#ffffff; margin:0 0 6px 0; line-height:1.25;">
          ${escapeHtml(job.whereWeAreStage || ("Stage " + st.phase + ": " + st.name))}
        </h3>
        <div style="background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:9999px; height:9px; width:100%; overflow:hidden; margin-bottom:11px; padding:1px;">
          <div style="height:100%; width:${pct}%; background:linear-gradient(90deg, #b8891e 0%, #d4af37 60%, #f3e5ab 100%); border-radius:9999px;"></div>
        </div>
      </div>

      <!-- Daily Field Write-Up Preview Box (Updates when any calendar date is clicked) -->
      <div style="background:#060910; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:11px 13px; display:flex; flex-direction:column; justify-content:space-between; gap:8px; flex:1;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:5px;">
            <div style="display:flex; align-items:center; gap:6px;">
              <span class="kp-badge-pill kp-badge-gold" style="font-size:0.63rem !important; padding:2px 8px !important;">
                ${dayInfo.isToday ? "TODAY'S WRITE-UP • OCT 15" : "DAILY WRITE-UP • OCT " + dayInfo.dayNum}
              </span>
              <span style="font-size:0.78rem; font-weight:900; color:#ffffff;">${escapeHtml(dayInfo.labelDate)}</span>
            </div>
            <div style="display:flex; align-items:center; gap:5px;">
              ${!dayInfo.isToday ? `<button type="button" onclick="selectMiniCalDay(15)" class="kp-secondary-btn kp-pill-sm" style="padding:2px 8px !important; min-height:22px !important; font-size:0.65rem !important;">&#8634; Today (Oct 15)</button>` : ""}
              <button type="button" onclick="promptEditDayWriteUpFromTab1(${dayInfo.dayNum})" class="kp-secondary-btn kp-pill-sm" style="padding:2px 8px !important; min-height:22px !important; font-size:0.65rem !important;">
                Edit Write-Up
              </button>
            </div>
          </div>

          <div style="font-size:0.72rem; font-weight:800; color:#d4af37; margin-bottom:4px;">
            ${escapeHtml(dayInfo.stage)} &bull; <span style="color:#cbd5e1; font-weight:700;">Crew: ${escapeHtml(dayInfo.crew)}</span>
          </div>

          <p style="font-size:0.78rem; line-height:1.5; color:#f8fafc !important; margin:0;">
            ${escapeHtml(dayInfo.writeUp)}
          </p>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; padding-top:7px; border-top:1px solid rgba(255,255,255,0.08); font-size:0.7rem; color:#94a3b8;">
          <span>Day Status: <strong style="color:#f3e5ab;">${escapeHtml(dayInfo.status)}</strong></span>
          <span>Stage 09 Spend: <strong style="color:#ffffff;">${fmtMoney(st.billed)} / ${fmtMoney(st.contract)}</strong> &bull; Stages 01–08: <strong style="color:#d4af37;">8/8 Done ($528,500)</strong></span>
        </div>
      </div>
    `;
  }

  const miniCalPanel = document.getElementById("p1-mini-month-calendar-panel");
  if (miniCalPanel) {
    const dows = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    let cellsHtml = dows.map(d => `<div class="kp-mini-cal-dow">${d}</div>`).join("");
    for (let empty = 0; empty < 4; empty++) {
      cellsHtml += `<div class="kp-mini-cal-day" style="opacity:0.15; pointer-events:none;"></div>`;
    }
    for (let day = 1; day <= 31; day++) {
      let cls = "kp-mini-cal-day";
      if (day === 15) {
        cls += " today-sit";
      } else if (day >= 12) {
        cls += " active-framing";
      } else {
        cls += " done-oct";
      }
      if (day === selectedTab1PreviewDay) {
        cls += " selected-day";
      }
      cellsHtml += `<div class="${cls}" onclick="selectMiniCalDay(${day})" title="Click to preview write-up for Oct ${day}, 2026">${day}</div>`;
    }

    miniCalPanel.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:4px;">
        <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.86rem; font-weight:900; color:#ffffff; letter-spacing:0.03em;">
          OCTOBER 2026 &mdash; CLICK DATE TO PREVIEW
        </div>
        <span class="kp-badge-pill kp-badge-gold" onclick="selectMiniCalDay(15)" style="font-size:0.62rem !important; padding:2px 8px !important; cursor:pointer;" title="Jump to Today (Oct 15)">
          Oct 15 &bull; Today
        </span>
      </div>
      <div class="kp-mini-cal-grid">
        ${cellsHtml}
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:8px; padding-top:6px; border-top:1px solid rgba(255,255,255,0.08); font-size:0.66rem; color:#cbd5e1;">
        <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:rgba(255,255,255,0.25);margin-right:4px;"></span>Oct 1&ndash;11: Steel Done</span>
        <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:#d4af37;margin-right:4px;"></span><strong>Selected: Oct ${selectedTab1PreviewDay}</strong></span>
        <span><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:rgba(212,175,55,0.35);border:1px solid #d4af37;margin-right:4px;"></span>Oct 12&ndash;31: Stage 09 Framing</span>
      </div>
    `;
  }

  // 4. Section 3: Update Section 3 Jurisdiction & Permit Badges + The 3 Master PDF Cards
  const sec3DistBadge = document.getElementById("p1-pdf-district-badge");
  if (sec3DistBadge) sec3DistBadge.innerText = "Submitted to: " + muniName;
  const sec3PermitBadge = document.getElementById("p1-pdf-permit-badge");
  if (sec3PermitBadge) sec3PermitBadge.innerText = "✓ City Building Permit #" + job.permitNum;

  const pdfGrid = document.getElementById("p1-master-pdfs-grid");
  if (pdfGrid) {
    const cName = job.contractPdfName || ("CCDC5B_Executed_Prime_Contract_" + job.jobId + ".pdf");
    const archPs = (job.planSets && job.planSets.arch) ? job.planSets.arch : {
      title: "Architectural Plans (AIBC)",
      firm: "Studio Vance Architecture AIBC",
      rev: "Rev 3 — IFC",
      pdfName: "KP-2026-001_Architect_AIBC_Full_Plans_IFC.pdf"
    };
    const engPs = (job.planSets && job.planSets.eng) ? job.planSets.eng : {
      title: "Structural & Geotech Engineering",
      firm: "Apex Structural P.Eng.",
      rev: "Rev 2 — Schedule B",
      pdfName: "KP-2026-001_Structural_Geotech_Engineering_Sealed.pdf"
    };

    pdfGrid.innerHTML = `
      <!-- 1. SIGNED PRIME CONTRACT PDF -->
      <div class="kp-pdf-master-card" onclick="openMasterPdfOnScreen('contract')">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:7px;">
            <span class="kp-badge-pill kp-badge-gold">1. SIGNED CONTRACT PDF</span>
            <span class="kp-badge-pill kp-badge-white">&#10003; Dual-Signed</span>
          </div>
          <div style="font-size:0.89rem; font-weight:900; color:#ffffff; line-height:1.3;">Signed CCDC 5B Prime Construction Contract</div>
          <div style="font-size:0.72rem; color:#cbd5e1; font-weight:600; margin:3px 0 7px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Wayne Stevenson (#52603) &times; ${escapeHtml(job.ownerName)}</div>
          <div class="kp-pdf-permit-bar">
            <span>${escapeHtml(muniName)}</span>
            <span>Permit #${escapeHtml(job.permitNum)}</span>
          </div>
          <div class="kp-pdf-file-pill" title="${escapeHtml(cName)}">
            PDF: ${escapeHtml(cName)}
          </div>
        </div>
        <div class="kp-pdf-btn-row" onclick="event.stopPropagation();">
          <button type="button" onclick="openMasterPdfOnScreen('contract')" class="kp-gold-btn kp-pill-sm" style="flex:1; justify-content:center;">
            Open PDF on Screen
          </button>
          <button type="button" onclick="downloadPrimaryContractPdf()" class="kp-secondary-btn kp-pill-sm" title="Download Contract PDF">
            Download
          </button>
        </div>
      </div>

      <!-- 2. ARCHITECT PLANS PDF (WITH CITY SUBMISSION & PERMIT NUMBER) -->
      <div class="kp-pdf-master-card" onclick="openMasterPdfOnScreen('arch')">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:7px;">
            <span class="kp-badge-pill kp-badge-gold">2. ARCHITECT PLANS PDF</span>
            <span class="kp-badge-pill kp-badge-white">&#10003; AIBC Sealed</span>
          </div>
          <div style="font-size:0.89rem; font-weight:900; color:#ffffff; line-height:1.3;">Architect Plans (AIBC Issued for Construction)</div>
          <div style="font-size:0.72rem; color:#cbd5e1; font-weight:600; margin:3px 0 7px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(archPs.firm)} &bull; Sheets A-101 to A-401</div>
          <div class="kp-pdf-permit-bar" title="Submitted to ${escapeHtml(muniName)} under Building Permit #${escapeHtml(job.permitNum)}">
            <span>City Filed: ${escapeHtml(muniName)}</span>
            <span>Permit #${escapeHtml(job.permitNum)}</span>
          </div>
          <div class="kp-pdf-file-pill" title="${escapeHtml(archPs.pdfName)}">
            PDF: ${escapeHtml(archPs.pdfName)}
          </div>
        </div>
        <div class="kp-pdf-btn-row" onclick="event.stopPropagation();">
          <button type="button" onclick="openMasterPdfOnScreen('arch')" class="kp-gold-btn kp-pill-sm" style="flex:1; justify-content:center;">
            Open PDF on Screen
          </button>
          <button type="button" onclick="downloadPlanSetPdf('arch')" class="kp-secondary-btn kp-pill-sm" title="Download Architect Plans PDF">
            Download
          </button>
        </div>
      </div>

      <!-- 3. ENGINEERING PLANS PDF (WITH CITY SUBMISSION & PERMIT NUMBER) -->
      <div class="kp-pdf-master-card" onclick="openMasterPdfOnScreen('eng')">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:7px;">
            <span class="kp-badge-pill kp-badge-gold">3. ENGINEERING PLANS PDF</span>
            <span class="kp-badge-pill kp-badge-white">&#10003; P.Eng. Schedule B</span>
          </div>
          <div style="font-size:0.89rem; font-weight:900; color:#ffffff; line-height:1.3;">Engineering Plans (Structural P.Eng. &amp; Geotech)</div>
          <div style="font-size:0.72rem; color:#cbd5e1; font-weight:600; margin:3px 0 7px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(engPs.firm)} &bull; Sheets S-101 to E-101</div>
          <div class="kp-pdf-permit-bar" title="Submitted to ${escapeHtml(muniName)} under Building Permit #${escapeHtml(job.permitNum)}">
            <span>City Filed: ${escapeHtml(muniName)}</span>
            <span>Permit #${escapeHtml(job.permitNum)}</span>
          </div>
          <div class="kp-pdf-file-pill" title="${escapeHtml(engPs.pdfName)}">
            PDF: ${escapeHtml(engPs.pdfName)}
          </div>
        </div>
        <div class="kp-pdf-btn-row" onclick="event.stopPropagation();">
          <button type="button" onclick="openMasterPdfOnScreen('eng')" class="kp-gold-btn kp-pill-sm" style="flex:1; justify-content:center;">
            Open PDF on Screen
          </button>
          <button type="button" onclick="downloadPlanSetPdf('eng')" class="kp-secondary-btn kp-pill-sm" title="Download Engineering Plans PDF">
            Download
          </button>
        </div>
      </div>
    `;
  }
}

function renderTab1RevisionsTable() {}


function signAndApproveRevision(tradeId, revId) {
  const job = getActiveJob();
  const trade = (job.trades || []).find(t => String(t.id) === String(tradeId));
  if (!trade) return;
  const rev = (trade.revisions || []).find(r => String(r.id) === String(revId));
  if (!rev) return;

  const signer = prompt("Enter Property Owner Full Legal Name to Digitally Sign & Approve Revision " + rev.id + " (" + fmtMoney(rev.amount) + "):", job.ownerName);
  if (!signer) return;

  rev.signed = true;
  rev.signedBy = signer.trim();
  rev.signedDate = new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" });
  saveState();
  renderAllPortalComponents();
  if (activeTradeModalId === trade.id) renderTradeModalRevisions(trade);
  showToast("✍️ Revision " + rev.id + " digitally signed by " + rev.signedBy + " & added to Revised Contract Sum!");
}

function downloadRevisionPdf(tradeId, revId) {
  const job = getActiveJob();
  const trade = (job.trades || []).find(t => String(t.id) === String(tradeId));
  const rev = trade ? (trade.revisions || []).find(r => String(r.id) === String(revId)) : null;
  if (!rev) return;
  const body = [
    "CHANGE ORDER / CONTRACT REVISION: " + rev.id,
    "TRADE AFFECTED: Stage " + trade.phase + " - " + trade.name + " (" + trade.sub + ")",
    "REVISION TITLE: " + rev.title,
    "SCOPE DESCRIPTION: " + rev.desc,
    "COST IMPACT: " + fmtMoney(rev.amount),
    "SCHEDULE IMPACT: +" + (rev.days || 0) + " Days",
    "OWNER SIGNATURE STATUS: " + (rev.signed ? ("SIGNED & APPROVED BY " + rev.signedBy + " ON " + rev.signedDate) : "PENDING OWNER SIGNATURE")
  ].join("\r\n");
  triggerDummyDownload(rev.pdfName || (rev.id + "_ChangeOrder.pdf"), body, rev.pdfDataUrl);
}

function openQuickAddRevisionModal() {
  const job = getActiveJob();
  const phaseNum = prompt("Enter Trade Stage # (01 to 30) for this Revision (e.g. 09 for Framing, 15 for Electrical, 21 for Millwork):", "09");
  if (!phaseNum) return;
  const trade = (job.trades || []).find(t => t.phase === phaseNum.padStart(2, "0")) || job.trades[0];
  const title = prompt("Enter Revision / Change Order Title (e.g. Upgrade Primary Deck to Covered Cedar Soffit):");
  if (!title) return;
  const desc = prompt("Enter Detailed Scope Modification Description:", "Owner requested architectural upgrade per revised drawing.");
  const amt = Number(prompt("Enter Cost Impact in $ CAD (e.g. 8500):", "8500")) || 0;
  const days = Number(prompt("Enter Schedule Impact in Days (e.g. 3):", "2")) || 0;

  const revId = "CO-00" + (Math.floor(Math.random() * 89) + 10);
  trade.revisions = trade.revisions || [];
  trade.revisions.push({
    id: revId,
    date: new Date().toISOString().slice(0, 10),
    title: title,
    desc: desc || title,
    amount: amt,
    days: days,
    pdfName: revId + "_" + title.replace(/[^a-zA-Z0-9]/g, "_").slice(0, 24) + ".pdf",
    signed: false,
    signedBy: "",
    signedDate: ""
  });
  saveState();
  renderAllPortalComponents();
  showToast("📑 Added Revision " + revId + " under Stage " + trade.phase + " (Ready for Owner Signature)");
}

function renderTab1DrawsTable() {
  const job = getActiveJob();
  const revStats = getJobSignedRevisionsSum(job);
  const revisedTotal = (Number(job.contractPrice) || 0) + revStats.signedSum;
  const tbody = document.getElementById("p1-draws-tbody");
  if (!tbody) return;

  tbody.innerHTML = (job.draws || []).map((d, idx) => {
    const gross = Math.round(revisedTotal * ((Number(d.pct) || 0) / 100));
    const hold = Math.round(gross * 0.10);
    const net = gross - hold;
    const badgeClass = d.status === "Paid" ? "kp-badge-cyan" : (d.status === "Due Now" ? "kp-badge-gold" : "kp-badge-amber");
    return `
      <tr>
        <td style="font-weight:900; color:#d4af37;">${escapeHtml(d.id)}</td>
        <td style="font-weight:700; color:#ffffff;">${escapeHtml(d.stage)}</td>
        <td>${escapeHtml(d.pct)}%</td>
        <td style="font-weight:800;">${fmtMoney(gross)}</td>
        <td style="color:#d4af37;">${fmtMoney(hold)}</td>
        <td style="font-weight:900; color:#38bdf8;">${fmtMoney(net)}</td>
        <td>
          <select onchange="updateDrawStatus(${idx}, this.value)" style="background:rgba(4,8,16,0.9); border:1px solid rgba(56,189,248,0.4); color:#fff; border-radius:9999px; padding:4px 10px; font-size:0.74rem; font-weight:800;">
            <option value="Paid" ${d.status === "Paid" ? "selected" : ""}>✓ Paid</option>
            <option value="Due Now" ${d.status === "Due Now" ? "selected" : ""}>⚡ Due Now</option>
            <option value="Scheduled" ${d.status === "Scheduled" ? "selected" : ""}>🔜 Scheduled</option>
          </select>
        </td>
        <td>
          <label class="kp-secondary-btn kp-pill-sm" style="cursor:pointer;">
            📤 Upload
            <input type="file" style="display:none;" onchange="handleDrawPdfUpload(${idx}, event)" />
          </label>
          <button type="button" onclick="downloadDrawPdf(${idx})" class="kp-cyan-btn kp-pill-sm">📥 ${escapeHtml(d.pdfName || (d.id + "_Invoice.pdf"))}</button>
        </td>
        <td style="text-align:right;">
          <button type="button" onclick="promptEditDrawRow(${idx})" class="kp-secondary-btn kp-pill-sm">✏️ Edit</button>
        </td>
      </tr>
    `;
  }).join("");
}

function updateDrawStatus(idx, val) {
  const job = getActiveJob();
  if (job.draws && job.draws[idx]) {
    job.draws[idx].status = val;
    saveState();
    renderTab1DrawsTable();
    showToast("Updated " + job.draws[idx].id + " status to " + val);
  }
}

function handleDrawPdfUpload(idx, ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.draws[idx].pdfName = file.name;
    job.draws[idx].pdfDataUrl = e.target.result;
    saveState();
    renderTab1DrawsTable();
    showToast("📤 Uploaded Draw PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadDrawPdf(idx) {
  const job = getActiveJob();
  const d = job.draws[idx];
  if (!d) return;
  triggerDummyDownload(d.pdfName || (d.id + "_Draw_Certificate.pdf"), "Construction Draw Milestone Certificate: " + d.stage, d.pdfDataUrl);
}

function promptEditDrawRow(idx) {
  const job = getActiveJob();
  const d = job.draws[idx];
  if (!d) return;
  const newStage = prompt("Edit Draw Milestone Description:", d.stage);
  if (!newStage) return;
  const newPct = Number(prompt("Edit % of Contract Price:", d.pct)) || d.pct;
  d.stage = newStage;
  d.pct = newPct;
  saveState();
  renderTab1DrawsTable();
}

function addPaymentDrawRow() {
  const job = getActiveJob();
  const stage = prompt("Enter New Draw Milestone Name:");
  if (!stage) return;
  const pct = Number(prompt("Enter % of Total Contract:", "10")) || 10;
  job.draws.push({
    id: "D-0" + (job.draws.length + 1),
    stage: stage,
    pct: pct,
    status: "Scheduled",
    pdfName: ""
  });
  saveState();
  renderTab1DrawsTable();
}

function promptEditContractPrice() {
  const job = getActiveJob();
  const val = prompt("Enter Original Baseline Contract Price ($ CAD) for " + job.address + ":", job.contractPrice);
  if (val === null) return;
  const num = Number(String(val).replace(/[^0-9.]/g, ""));
  if (num > 0) {
    job.contractPrice = num;
    saveState();
    renderAllPortalComponents();
    showToast("💰 Updated Original Contract Price to " + fmtMoney(num));
  }
}

function promptEditOwnerDetails() {
  const job = getActiveJob();
  const name = prompt("Enter Property Owner Full Name(s):", job.ownerName);
  if (!name) return;
  const phone = prompt("Enter Property Owner Phone (SMS / Call):", job.ownerPhone) || job.ownerPhone;
  const email = prompt("Enter Property Owner Email:", job.ownerEmail) || job.ownerEmail;
  const pass = prompt("Enter Property Owner Login Passcode for this Job:", job.ownerPasscode) || job.ownerPasscode;
  job.ownerName = name;
  job.ownerPhone = phone;
  job.ownerEmail = email;
  job.ownerPasscode = pass;
  saveState();
  renderAllPortalComponents();
  showToast("✅ Updated Property Owner credentials for " + job.address);
}

function promptEditJobIdentity() {
  const job = getActiveJob();
  const addr = prompt("Edit Job Civic Address:", job.address);
  if (!addr) return;
  const price = Number(prompt("Edit Original Contract Price ($ CAD):", job.contractPrice)) || job.contractPrice;
  const scope = prompt("Edit Executive Scope Note:", job.scopeSummary) || job.scopeSummary;
  job.address = addr;
  job.contractPrice = price;
  job.scopeSummary = scope;
  saveState();
  renderAllPortalComponents();
  showToast("✅ Updated Job Identity & Contract Scope");
}

function handleContractPdfUpload(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.contractPdf = {
      name: file.name,
      date: new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" }),
      size: Math.max(1, Math.round(file.size / 1024)) + " KB",
      dataUrl: e.target.result
    };
    saveState();
    renderTab1Contract();
    showToast("📤 Uploaded Executed Contract PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadPrimaryContractPdf() {
  const job = getActiveJob();
  const revStats = getJobSignedRevisionsSum(job);
  const body = [
    "CCDC 5B / PRIME CONSTRUCTION CONTRACT — EXECUTED COPY",
    "JOB ADDRESS: " + job.address + " (" + job.jobId + ")",
    "BUILDER: Keystone Possibilities Ltd. — Wayne Stevenson (BC Housing #52603)",
    "PROPERTY OWNER: " + job.ownerName + " (" + job.ownerPhone + ")",
    "ORIGINAL CONTRACT SUM: " + fmtMoney(job.contractPrice),
    "APPROVED REVISIONS: " + fmtMoney(revStats.signedSum),
    "REVISED CONTRACT TOTAL: " + fmtMoney(job.contractPrice + revStats.signedSum),
    "BUILDER SIGNATURE: " + job.builderSig.name + " (" + job.builderSig.date + ")",
    "OWNER SIGNATURE: " + (job.ownerSig.signed ? (job.ownerSig.typedName + " (" + job.ownerSig.date + ")") : "Pending")
  ].join("\r\n");
  triggerDummyDownload(job.contractPdf.name, body, job.contractPdf.dataUrl);
  showToast("📥 Downloading " + job.contractPdf.name);
}

function previewPrimaryContractModal() {
  const job = getActiveJob();
  const revStats = getJobSignedRevisionsSum(job);
  const revisedTotal = (Number(job.contractPrice) || 0) + revStats.signedSum;
  document.getElementById("pdf-modal-title").innerHTML = `<span>📜</span> ${escapeHtml(job.contractPdf.name)}`;
  document.getElementById("pdf-modal-body").innerHTML = `
    <div style="background:#050914; border:1px solid rgba(212,175,55,0.45); border-radius:14px; padding:24px; color:#e2e8f0; line-height:1.6;">
      <div style="display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.12); padding-bottom:14px; margin-bottom:16px; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.25rem; font-weight:900; color:#d4af37;">KEYSTONE POSSIBILITIES LTD. — PRIME CONSTRUCTION AGREEMENT</div>
          <div style="font-size:0.82rem; color:#38bdf8;">Job Address: ${escapeHtml(job.address)} &bull; Ref: ${escapeHtml(job.jobId)} &bull; Permit: ${escapeHtml(job.permitNum)}</div>
        </div>
        <span class="kp-badge-pill kp-badge-cyan">BC Housing Licensed Builder #52603</span>
      </div>
      <p><strong>BETWEEN BUILDER:</strong> Keystone Possibilities Ltd. (Wayne Stevenson, Licensed Residential Builder #52603, BC Hydro Civil ES54)</p>
      <p><strong>AND PROPERTY OWNER(S):</strong> ${escapeHtml(job.ownerName)} (${escapeHtml(job.ownerPhone)} &bull; ${escapeHtml(job.ownerEmail)})</p>
      <p><strong>1. CONTRACT PRICE &amp; REVISIONS:</strong> Original Baseline Price: <strong>${fmtMoney(job.contractPrice)} CAD</strong> | Signed Revisions: <strong>${fmtMoney(revStats.signedSum)} CAD</strong> | Revised Total Contract Sum: <strong style="color:#d4af37;">${fmtMoney(revisedTotal)} CAD</strong>.</p>
      <p><strong>2. STATUTORY 10% BUILDERS LIEN ACT HOLDBACK:</strong> Pursuant to Section 5 of the BC Builders Lien Act, a 10% statutory holdback (${fmtMoney(revisedTotal * 0.10)}) is retained in trust and released following the 55-day statutory completion period.</p>
      <p><strong>3. 2-5-10 NATIONAL HOME WARRANTY:</strong> Enrolled under Policy #${escapeHtml(job.warranty.policyNum)} (2-Year Materials &amp; Labour, 5-Year Building Envelope, 10-Year Structural Integrity).</p>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:20px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.12);">
        <div>
          <div style="font-size:0.72rem; color:#94a3b8;">BUILDER SIGNATURE:</div>
          <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.25rem; color:#d4af37; font-style:italic;">${escapeHtml(job.builderSig.name)}</div>
          <div style="font-size:0.75rem; color:#38bdf8;">✓ Signed ${escapeHtml(job.builderSig.date)}</div>
        </div>
        <div>
          <div style="font-size:0.72rem; color:#94a3b8;">PROPERTY OWNER SIGNATURE:</div>
          <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.25rem; color:#38bdf8; font-style:italic;">${escapeHtml(job.ownerSig.typedName)}</div>
          <div style="font-size:0.75rem; color:#d4af37;">✓ Signed ${escapeHtml(job.ownerSig.date)}</div>
        </div>
      </div>
    </div>
  `;
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (dlBtn) dlBtn.onclick = () => downloadPrimaryContractPdf();
  openModal("modal-pdf-viewer");
}

function printExecutedContractDocument() {
  previewPrimaryContractModal();
  setTimeout(() => window.print(), 350);
}

function handleVaultUpload(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.vaultDocs.unshift({
      title: file.name,
      desc: "Uploaded Contract Addendum (" + Math.max(1, Math.round(file.size / 1024)) + " KB)",
      date: new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" }),
      dataUrl: e.target.result
    });
    saveState();
    renderTab1Contract();
    showToast("📤 Attached Addendum PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function previewVaultDocModal(idx) {
  const job = getActiveJob();
  const doc = job.vaultDocs[idx];
  if (!doc) return;
  document.getElementById("pdf-modal-title").innerHTML = `<span>📑</span> ${escapeHtml(doc.title)}`;
  document.getElementById("pdf-modal-body").innerHTML = `
    <div style="background:#050914; border:1px solid rgba(56,189,248,0.4); border-radius:14px; padding:22px; color:#e2e8f0;">
      <h4 style="color:#d4af37; margin:0 0 8px 0;">${escapeHtml(doc.title)}</h4>
      <p style="color:#94a3b8; font-size:0.84rem;">${escapeHtml(doc.desc)} &bull; Job: ${escapeHtml(job.address)}</p>
      <div style="padding:14px; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.3); border-radius:10px; font-size:0.82rem; color:#38bdf8;">
        ✓ Verified &amp; Logged to Job Repository ${escapeHtml(job.jobId)} under Superintendent Wayne Stevenson (#52603).
      </div>
    </div>
  `;
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (dlBtn) dlBtn.onclick = () => downloadVaultDoc(idx);
  openModal("modal-pdf-viewer");
}

function downloadVaultDoc(idx) {
  const job = getActiveJob();
  const doc = job.vaultDocs[idx];
  if (!doc) return;
  triggerDummyDownload(doc.title, doc.desc, doc.dataUrl);
}

// Interactive HTML5 Signature Pad
let sigCanvasHasDrawing = false;
function initSignaturePadCanvas() {
  const canvas = document.getElementById("p1-owner-sig-canvas");
  if (!canvas || canvas.__kpSigBound) return;
  canvas.__kpSigBound = true;
  const ctx = canvas.getContext("2d");
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2.4;
  ctx.lineCap = "round";
  let drawing = false;

  function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height)
    };
  }
  canvas.addEventListener("mousedown", (e) => { drawing = true; sigCanvasHasDrawing = true; const p = getPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); });
  canvas.addEventListener("mousemove", (e) => { if (!drawing) return; const p = getPos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); });
  window.addEventListener("mouseup", () => { drawing = false; });
  canvas.addEventListener("touchstart", (e) => { e.preventDefault(); drawing = true; sigCanvasHasDrawing = true; const p = getPos(e); ctx.beginPath(); ctx.moveTo(p.x, p.y); }, { passive: false });
  canvas.addEventListener("touchmove", (e) => { if (!drawing) return; e.preventDefault(); const p = getPos(e); ctx.lineTo(p.x, p.y); ctx.stroke(); }, { passive: false });
  window.addEventListener("touchend", () => { drawing = false; });
}

function clearOwnerSignatureCanvas() {
  const canvas = document.getElementById("p1-owner-sig-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  sigCanvasHasDrawing = false;
}

function applyOwnerContractSignature() {
  const job = getActiveJob();
  const typedInput = document.getElementById("p1-owner-sig-typed");
  const typedName = (typedInput && typedInput.value.trim()) ? typedInput.value.trim() : job.ownerName;
  const canvas = document.getElementById("p1-owner-sig-canvas");
  const dataUrl = (canvas && sigCanvasHasDrawing) ? canvas.toDataURL("image/png") : "";

  job.ownerSig = {
    signed: true,
    typedName: typedName,
    date: new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" }),
    dataUrl: dataUrl
  };
  saveState();
  renderTab1Contract();
  showToast("✍️ Property Owner Signature Applied & Sealed on Master Contract!");
}

function promptUpdateBuilderSignature() {
  const job = getActiveJob();
  const name = prompt("Confirm Builder Signatory Name:", job.builderSig.name || "Wayne Stevenson");
  if (!name) return;
  job.builderSig.name = name;
  job.builderSig.date = new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" });
  saveState();
  renderTab1Contract();
  showToast("✍️ Updated Builder Signature Seal");
}

// ============================================================================
// 6. TAB 2: LIVE CALENDAR, "WHERE WE ARE NOW" & ACTIVE TRADES RADAR
// ============================================================================
let calMonth = 9; // October (0-indexed)
let calYear = 2026;
let activeModalDateStr = "2026-10-15";


const KP_MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function computeTradePctDone(job, t) {
  if (typeof t.pctDone === "number" && !isNaN(t.pctDone)) {
    return Math.min(100, Math.max(0, Math.round(t.pctDone)));
  }
  if (String(t.phase) === "09") {
    return Math.min(100, Math.max(1, Number(job.whereWeArePct) || 48));
  }
  if (t.status === "Completed") return 100;
  if (t.contract > 0 && t.billed > 0) {
    return Math.min(100, Math.round((t.billed / t.contract) * 100));
  }
  return 0;
}

function renderWhereWeAreBar() {
  const job = getActiveJob();
  const dateStr = job.whereWeAreDate || "2026-10-15";
  const dateInput = document.getElementById("p2-where-we-are-date");
  if (dateInput) dateInput.value = dateStr;
  const datePill = document.getElementById("p2-current-date-pill");
  if (datePill) datePill.innerText = "Active Date: " + dateStr;
  const stageHead = document.getElementById("p2-current-stage-headline");
  if (stageHead) stageHead.innerText = `${job.whereWeAreStage} (${job.whereWeArePct}% Complete)`;
  const fill = document.getElementById("p2-progress-bar-fill");
  if (fill) fill.style.width = Math.min(100, Math.max(2, Number(job.whereWeArePct) || 48)) + "%";
  const radarDate = document.getElementById("p2-radar-date-label");
  if (radarDate) radarDate.innerText = dateStr;
}

function setQuickBuildStage(stageTitle, pct) {
  const job = getActiveJob();
  job.whereWeAreStage = stageTitle;
  job.whereWeArePct = pct;
  saveState();
  renderWhereWeAreBar();
  renderTab1Contract();
  renderActiveTradeRadar();
  showToast("Updated Active Build Stage: " + stageTitle + " (" + pct + "%)");
}

function updateWhereWeAreDate(newDateStr) {
  if (!newDateStr) return;
  const job = getActiveJob();
  job.whereWeAreDate = newDateStr;
  const parts = newDateStr.split("-");
  if (parts.length === 3) {
    calYear = Number(parts[0]);
    calMonth = Number(parts[1]) - 1;
  }
  saveState();
  renderWhereWeAreBar();
  renderTab1Contract();
  renderCalendar();
  renderActiveTradeRadar();
  showToast("Active Date updated to " + newDateStr);
}

function promptUpdateWhereWeAreStage() {
  const job = getActiveJob();
  const stg = prompt("Enter Current Active Construction Stage Headline:", job.whereWeAreStage);
  if (!stg) return;
  const pct = Number(prompt("Enter Stage Completion % (1 to 100):", job.whereWeArePct)) || job.whereWeArePct;
  job.whereWeAreStage = stg;
  job.whereWeArePct = Math.min(100, Math.max(1, pct));
  saveState();
  renderWhereWeAreBar();
  renderTab1Contract();
  renderActiveTradeRadar();
  showToast("Updated Stage & Completion %");
}

function jumpToWhereWeAreMonth() {
  const job = getActiveJob();
  const parts = (job.whereWeAreDate || "2026-10-15").split("-");
  if (parts.length === 3) {
    calYear = Number(parts[0]);
    calMonth = Number(parts[1]) - 1;
  }
  renderCalendar();
}

function navigateMonth(delta) {
  calMonth += delta;
  if (calMonth < 0) { calMonth = 11; calYear--; }
  if (calMonth > 11) { calMonth = 0; calYear++; }
  renderCalendar();
}

function onCalendarSelectChange() {
  const mSel = document.getElementById("cal-month-select");
  const ySel = document.getElementById("cal-year-select");
  if (mSel) calMonth = Number(mSel.value);
  if (ySel) calYear = Number(ySel.value);
  renderCalendar();
}

function renderCalendar() {
  const job = getActiveJob();
  const mSel = document.getElementById("cal-month-select");
  const ySel = document.getElementById("cal-year-select");
  if (mSel) mSel.value = String(calMonth);
  if (ySel) ySel.value = String(calYear);

  const dateInput = document.getElementById("p2-where-we-are-date");
  if (dateInput) dateInput.value = job.whereWeAreDate || "2026-10-15";

  const grid = document.getElementById("kp-calendar-days");
  if (!grid) return;
  grid.innerHTML = "";

  const firstDay = new Date(calYear, calMonth, 1).getDay();
  const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();

  for (let i = 0; i < firstDay; i++) {
    const empty = document.createElement("div");
    empty.className = "kp-cal-day";
    empty.style.opacity = "0.22";
    empty.style.pointerEvents = "none";
    grid.appendChild(empty);
  }

  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
    const isWhereWeAre = (dateStr === (job.whereWeAreDate || "2026-10-15"));
    const cell = document.createElement("div");
    cell.className = "kp-cal-day" + (isWhereWeAre ? " where-we-are" : "");
    cell.onclick = () => openDayModal(dateStr);

    // Strictly White-on-Black Event Pills (Zero Multi-Color Clutter)
    const pills = [];

    (job.trades || []).forEach(t => {
      if (t.startDate === dateStr) {
        pills.push(`<div class="kp-cal-event-pill">Start: Stage ${escapeHtml(t.phase)} ${escapeHtml(t.name.slice(0, 18))}</div>`);
      } else if (t.endDate === dateStr) {
        pills.push(`<div class="kp-cal-event-pill">Finish: Stage ${escapeHtml(t.phase)} ${escapeHtml(t.name.slice(0, 16))}</div>`);
      } else if (t.startDate && t.endDate && dateStr > t.startDate && dateStr < t.endDate && (d % 3 === 0 || isWhereWeAre)) {
        const pct = computeTradePctDone(job, t);
        pills.push(`<div class="kp-cal-event-pill">Stage ${escapeHtml(t.phase)}: ${escapeHtml(t.name.slice(0, 16))} (${pct}%)</div>`);
      }
    });

    (job.inspections || []).forEach(ins => {
      if (ins.date === dateStr) {
        pills.push(`<div class="kp-cal-event-pill">Inspection: ${escapeHtml(ins.title.slice(0, 19))}</div>`);
      }
    });

    const dayLog = (job.calendarLogs || {})[dateStr];
    const hasCustomNotes = dayLog && (dayLog.notes || (dayLog.photos && dayLog.photos.length));
    if (hasCustomNotes) {
      const fCount = (dayLog.photos || []).length;
      pills.push(`<div class="kp-cal-event-pill">Daily Log${fCount ? " (" + fCount + " file" + (fCount > 1 ? "s" : "") + ")" : ""}</div>`);
    }

    cell.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
        <span style="font-size:0.8rem; font-weight:900; color:#ffffff;">${d}</span>
        ${isWhereWeAre ? `<span style="background:#ffffff; color:#05070b; font-size:0.56rem; font-weight:900; padding:1px 6px; border-radius:9999px; letter-spacing:0.04em;">ACTIVE</span>` : ""}
      </div>
      ${pills.slice(0, 3).join("")}
      ${pills.length > 3 ? `<div style="font-size:0.62rem; color:#cbd5e1;">+${pills.length - 3} more</div>` : ""}
    `;
    grid.appendChild(cell);
  }

  renderActiveTradeRadar();
}

function renderActiveTradeRadar() {
  const job = getActiveJob();
  const activeListEl = document.getElementById("p2-active-trades-list");
  if (!activeListEl) return;

  const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
  const monthStart = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-01`;
  const monthEnd = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-${String(daysInMonth).padStart(2, "0")}`;
  const monthLabel = `${KP_MONTH_NAMES[calMonth] || "October"} ${calYear}`;

  const mBadge = document.getElementById("p2-active-trades-month-badge");
  if (mBadge) mBadge.innerText = monthLabel.toUpperCase();

  const mHead = document.getElementById("p2-active-trades-heading");
  if (mHead) mHead.innerText = `Active Trades This Month (${monthLabel})`;

  // Filter strictly to trades active in the selected calendar month
  const monthlyTrades = (job.trades || []).filter(t =>
    t.startDate && t.endDate && t.startDate <= monthEnd && t.endDate >= monthStart
  );

  const countBadge = document.getElementById("p2-active-trades-count");
  if (countBadge) {
    countBadge.innerText = `${monthlyTrades.length} Active Trade${monthlyTrades.length === 1 ? "" : "s"}`;
  }

  if (!monthlyTrades.length) {
    activeListEl.innerHTML = `
      <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:14px 16px; color:#cbd5e1; font-size:0.8rem;">
        No trades scheduled in ${escapeHtml(monthLabel)}. Select another month above or adjust trade dates in Tab 4.
      </div>
    `;
    return;
  }

  activeListEl.innerHTML = monthlyTrades.map(t => {
    const pct = computeTradePctDone(job, t);
    return `
      <div class="kp-monthly-trade-row" onclick="openTradeModal(${t.id})" title="Click to inspect or update trade details & schedule">
        <div style="min-width:0;">
          <div style="font-size:0.86rem; font-weight:900; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            Stage ${escapeHtml(t.phase)} &mdash; ${escapeHtml(t.name)}
          </div>
          <div style="font-size:0.74rem; color:#cbd5e1; margin-top:3px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            ${escapeHtml(t.sub)} (${escapeHtml(t.contact || "Site Foreman")}) &bull; ${escapeHtml(t.startDate)} to ${escapeHtml(t.endDate)}
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:10px;">
          <div style="flex:1; background:rgba(255,255,255,0.1); height:7px; border-radius:9999px; overflow:hidden; border:1px solid rgba(255,255,255,0.14);">
            <div style="width:${pct}%; height:100%; background:#ffffff; border-radius:9999px;"></div>
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#05070b; border:1px solid rgba(255,255,255,0.32); color:#ffffff; font-size:0.78rem; font-weight:900; padding:5px 13px; border-radius:9999px; white-space:nowrap; font-variant-numeric:tabular-nums;">
            ${pct}% Done
          </span>
        </div>
      </div>
    `;
  }).join("");
}

function openDayModal(dateStr) {
  activeModalDateStr = dateStr;
  const job = getActiveJob();
  job.calendarLogs = job.calendarLogs || {};
  if (!job.calendarLogs[dateStr]) {
    const autoTrades = (job.trades || [])
      .filter(t => t.startDate && t.endDate && dateStr >= t.startDate && dateStr <= t.endDate)
      .map(t => "Stage " + t.phase + ": " + t.sub);
    let defaultNotes = "";
    let defaultCheckpoints = [];
    if (dateStr.startsWith("2026-10-") && typeof getDayLogForOct2026 === "function") {
      const dNum = Number(dateStr.split("-")[2]);
      const octEntry = getDayLogForOct2026(job, dNum);
      if (octEntry && octEntry.text) defaultNotes = octEntry.text;
      defaultCheckpoints = [
        { text: "Daily Superintendent safety & quality walkthrough completed", done: dNum <= 15 },
        { text: "Subcontractor crew count & material deliveries logged", done: dNum <= 15 }
      ];
    }
    job.calendarLogs[dateStr] = {
      notes: defaultNotes,
      checkpoints: defaultCheckpoints,
      trades: autoTrades,
      photos: []
    };
  } else if (!job.calendarLogs[dateStr].notes && dateStr.startsWith("2026-10-") && typeof getDayLogForOct2026 === "function") {
    const dNum = Number(dateStr.split("-")[2]);
    const octEntry = getDayLogForOct2026(job, dNum);
    if (octEntry && octEntry.text) job.calendarLogs[dateStr].notes = octEntry.text;
  }

  const log = job.calendarLogs[dateStr];
  const titleEl = document.getElementById("day-modal-title");
  if (titleEl) {
    titleEl.innerHTML = `Daily Field Log &amp; File Storage &mdash; ${escapeHtml(dateStr)} (${escapeHtml(job.address)})`;
  }
  const notesEl = document.getElementById("day-notes-input");
  if (notesEl) notesEl.value = log.notes || "";
  renderDayModalInternals();
  openModal("modal-day");
}

function setModalDateAsWhereWeAre() {
  updateWhereWeAreDate(activeModalDateStr);
  closeModal("modal-day");
}

function renderDayModalInternals() {
  const job = getActiveJob();
  const log = (job.calendarLogs || {})[activeModalDateStr];
  if (!log) return;

  const cpList = document.getElementById("day-checkpoints-list");
  if (cpList) {
    cpList.innerHTML = (log.checkpoints || []).length ? (log.checkpoints || []).map((cp, i) => `
      <label style="display:flex; align-items:center; justify-content:space-between; gap:8px; background:#0b0f17; border:1px solid rgba(255,255,255,0.14); padding:7px 11px; border-radius:8px; font-size:0.78rem; color:#ffffff; cursor:pointer;">
        <span style="display:flex; align-items:center; gap:8px;">
          <input type="checkbox" ${cp.done ? "checked" : ""} onchange="toggleDayCheckpoint(${i})" />
          <span style="${cp.done ? "text-decoration:line-through; color:#cbd5e1;" : "color:#ffffff;"}">${escapeHtml(cp.text)}</span>
        </span>
        <span style="font-size:0.66rem; color:#cbd5e1; font-weight:700;">${cp.done ? "Done" : "Open"}</span>
      </label>
    `).join("") : `<div style="font-size:0.74rem; color:#94a3b8;">No checkpoints added yet for this date.</div>`;
  }

  const trTags = document.getElementById("day-trades-tags");
  if (trTags) {
    trTags.innerHTML = (log.trades || []).length ? (log.trades || []).map((tr, i) => `
      <span class="kp-badge-pill kp-badge-white" style="text-transform:none; font-size:0.72rem;">
        ${escapeHtml(tr)}
        <strong onclick="removeDayTradeTag(${i})" style="cursor:pointer; margin-left:6px; color:#ffffff;" title="Remove trade tag">&times;</strong>
      </span>
    `).join("") : `<span style="font-size:0.74rem; color:#94a3b8;">No trades tagged on this date.</span>`;
  }

  const phList = document.getElementById("day-photos-list");
  if (phList) {
    phList.innerHTML = (log.photos || []).length ? (log.photos || []).map((p, i) => `
      <div style="display:flex; justify-content:space-between; align-items:center; background:#05070b; border:1px solid rgba(255,255,255,0.16); padding:7px 10px; border-radius:8px; font-size:0.76rem; color:#ffffff;">
        <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:260px;">File: ${escapeHtml(p.name)}</span>
        <div style="display:flex; gap:6px; align-items:center;">
          <button type="button" onclick="triggerDummyDownload('${escapeHtml(p.name)}','Site File', '${p.dataUrl || ""}')" class="kp-secondary-btn kp-pill-sm">Download</button>
          <button type="button" onclick="removeDayPhoto(${i})" class="kp-secondary-btn kp-pill-sm" title="Remove stored file">&times;</button>
        </div>
      </div>
    `).join("") : `<div style="font-size:0.74rem; color:#94a3b8; padding:4px 0;">No files stored for this date yet. Click "Upload File" above to store PDFs or site photos.</div>`;
  }
}

function addDayCheckpointInline() {
  const inp = document.getElementById("new-checkpoint-input");
  if (!inp || !inp.value.trim()) return;
  const job = getActiveJob();
  job.calendarLogs[activeModalDateStr].checkpoints.push({ text: inp.value.trim(), done: true });
  inp.value = "";
  saveState();
  renderDayModalInternals();
}

function toggleDayCheckpoint(i) {
  const job = getActiveJob();
  const cp = job.calendarLogs[activeModalDateStr].checkpoints[i];
  if (cp) cp.done = !cp.done;
  saveState();
  renderDayModalInternals();
}

function addDayTradeInline() {
  const inp = document.getElementById("new-day-trade-input");
  if (!inp || !inp.value.trim()) return;
  const job = getActiveJob();
  job.calendarLogs[activeModalDateStr].trades.push(inp.value.trim());
  inp.value = "";
  saveState();
  renderDayModalInternals();
}

function removeDayTradeTag(i) {
  const job = getActiveJob();
  job.calendarLogs[activeModalDateStr].trades.splice(i, 1);
  saveState();
  renderDayModalInternals();
}

function removeDayPhoto(i) {
  const job = getActiveJob();
  if (job.calendarLogs && job.calendarLogs[activeModalDateStr] && job.calendarLogs[activeModalDateStr].photos) {
    job.calendarLogs[activeModalDateStr].photos.splice(i, 1);
    saveState();
    renderDayModalInternals();
    renderCalendar();
  }
}

function handleDayFileUpload(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.calendarLogs[activeModalDateStr].photos.push({ name: file.name, desc: "Site File", dataUrl: e.target.result });
    saveState();
    renderDayModalInternals();
    renderCalendar();
    showToast("Stored " + file.name + " in " + activeModalDateStr);
  };
  reader.readAsDataURL(file);
}

function saveDayLogModal() {
  const job = getActiveJob();
  const notesVal = (document.getElementById("day-notes-input") || {}).value || "";
  job.calendarLogs[activeModalDateStr].notes = notesVal;
  // Also sync to job.dayLogs so Page 1's daily write-up preview reflects any edits made on Page 2
  job.dayLogs = job.dayLogs || {};
  const existing = job.dayLogs[activeModalDateStr] || {};
  job.dayLogs[activeModalDateStr] = {
    title: existing.title || ("Field Log — " + activeModalDateStr),
    status: existing.status || "Updated via Live Calendar",
    trade: existing.trade || ((job.calendarLogs[activeModalDateStr].trades || [])[0] || "Stage 09 — Rough Wood Framing"),
    text: notesVal
  };
  saveState();
  closeModal("modal-day");
  renderCalendar();
  renderTab1Contract();
  showToast("Saved Daily Site Log for " + activeModalDateStr);
}



let activeP3Discipline = "city";

function getWarrantyTierDocs(job) {
  const w = job.warranty || {};
  job.warrantyTiers = job.warrantyTiers || {
    "2yr": {
      code: "2-YEAR",
      badge: "Materials & Labour",
      title: "12-Month & 24-Month Mechanical & Interior Coverage",
      desc: "12 Months: All defects in materials and labour (millwork, flooring, drywall, trim, hardware). 24 Months: Plumbing, HVAC/Hydronics, Electrical switchgear & BC Building Code compliance.",
      pdfName: "NHW_2Year_Materials_Labour_Certificate_" + job.jobId + ".pdf",
      dataUrl: ""
    },
    "5yr": {
      code: "5-YEAR",
      badge: "Building Envelope",
      title: "Complete Rainscreen, Window, Roof & Air Barrier Protection",
      desc: "Full 60-month coverage against unintended water penetration, building envelope failure, exterior cladding/rainscreen defects, roofing membranes, and triple-pane window perimeter seals.",
      pdfName: "NHW_5Year_Building_Envelope_Certificate_" + job.jobId + ".pdf",
      dataUrl: ""
    },
    "10yr": {
      code: "10-YEAR",
      badge: "Structural Integrity",
      title: "Load-Bearing Foundations, Shear Walls & Structural Frame",
      desc: "Full 120-month structural defects coverage on 35 MPa concrete footings/grade beams, bedrock anchors, Simpson Strong-Tie ATS shear systems, engineered floor joists, and roof trusses.",
      pdfName: "NHW_10Year_Structural_Integrity_Certificate_" + job.jobId + ".pdf",
      dataUrl: ""
    }
  };
  return job.warrantyTiers;
}

function openWarrantyTierPdfOnScreen(tierKey) {
  const job = getActiveJob();
  const w = job.warranty || {};
  const tiers = getWarrantyTierDocs(job);
  const muniName = resolveJobMunicipality(job);
  const t = tiers[tierKey] || {
    code: "2-5-10 MASTER",
    badge: "Complete Policy",
    title: "2-5-10 Year National Home Warranty Master Policy Certificate",
    desc: "Complete statutory 2-Year Materials & Labour, 5-Year Building Envelope, and 10-Year Structural Integrity protection under the BC Homeowner Protection Act.",
    pdfName: w.pdfName || ("National_Home_Warranty_2-5-10_Certificate_" + job.jobId + ".pdf")
  };

  const titleEl = document.getElementById("pdf-modal-title");
  const bodyEl = document.getElementById("pdf-modal-body");
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (!titleEl || !bodyEl || !dlBtn) return;

  titleEl.innerHTML = `<span>📄</span> ${escapeHtml(t.code)} Warranty Certificate PDF &mdash; ${escapeHtml(t.pdfName)}`;
  dlBtn.onclick = () => downloadWarrantyTierPdf(tierKey);

  bodyEl.innerHTML = `
    <div class="kp-pdf-page-sheet">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
        <div>
          <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.12em; text-transform:uppercase; color:#b45309;">BC HOMEOWNER PROTECTION ACT &bull; STATUTORY WARRANTY CERTIFICATE</div>
          <h1 style="font-size:1.35rem; font-weight:900; color:#0f172a; margin:4px 0;">${escapeHtml(t.code)} NATIONAL HOME WARRANTY CERTIFICATE (${escapeHtml(t.badge.toUpperCase())})</h1>
          <div style="font-size:0.84rem; color:#334155; font-weight:600;">Policy #${escapeHtml(w.policyNum)} &bull; ${escapeHtml(w.provider)}</div>
        </div>
        <div style="text-align:right; font-size:0.78rem; color:#334155;">
          <div><strong>Certificate File:</strong> ${escapeHtml(t.pdfName)}</div>
          <div><strong>Builder License:</strong> BC Housing #52603</div>
          <div><strong>Municipal Permit:</strong> #${escapeHtml(job.permitNum)} (${escapeHtml(muniName)})</div>
        </div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:20px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:14px;">
        <div>
          <div style="font-size:0.7rem; font-weight:800; text-transform:uppercase; color:#64748b;">Licensed Residential Builder</div>
          <div style="font-size:0.95rem; font-weight:800; color:#0f172a;">Keystone Possibilities Ltd. (Wayne Stevenson)</div>
          <div style="font-size:0.8rem; color:#334155;">BC Housing Licensed Builder #52603</div>
        </div>
        <div>
          <div style="font-size:0.7rem; font-weight:800; text-transform:uppercase; color:#64748b;">Registered Property Owner(s) &amp; Civic Address</div>
          <div style="font-size:0.95rem; font-weight:800; color:#0f172a;">${escapeHtml(job.ownerName)}</div>
          <div style="font-size:0.8rem; color:#334155;">${escapeHtml(job.address)} (PID: ${escapeHtml(job.pid)})</div>
        </div>
      </div>

      <h3 style="font-size:0.92rem; font-weight:800; text-transform:uppercase; color:#0f172a; border-bottom:1px solid #cbd5e1; padding-bottom:6px;">Coverage Specification &mdash; ${escapeHtml(t.title)}</h3>
      <p style="font-size:0.85rem; line-height:1.65; color:#1e293b; margin-bottom:20px;">
        ${escapeHtml(t.desc)}
      </p>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-top:26px; padding-top:18px; border-top:2px solid #0f172a;">
        <div>
          <div style="font-size:0.72rem; font-weight:800; text-transform:uppercase; color:#64748b;">Certified By Licensed Builder (#52603)</div>
          <div style="font-family:Georgia, serif; font-size:1.25rem; font-style:italic; font-weight:700; color:#0f172a; margin:8px 0 4px 0;">Wayne Stevenson</div>
          <div style="font-size:0.8rem; color:#334155;">Wayne Stevenson, President &mdash; Keystone Possibilities Ltd.</div>
        </div>
        <div>
          <div style="font-size:0.72rem; font-weight:800; text-transform:uppercase; color:#64748b;">Registered Property Owner Co-Sign</div>
          <div style="font-family:Georgia, serif; font-size:1.25rem; font-style:italic; font-weight:700; color:#0f172a; margin:8px 0 4px 0;">${escapeHtml(job.ownerName)}</div>
          <div style="font-size:0.8rem; color:#334155;">Policy #${escapeHtml(w.policyNum)} &bull; ${escapeHtml(w.status)}</div>
        </div>
      </div>
    </div>
  `;
  openModal("modal-pdf-viewer");
}

function downloadWarrantyTierPdf(tierKey) {
  const job = getActiveJob();
  const w = job.warranty || {};
  if (tierKey === "master") {
    downloadWarrantyCertificatePdf();
    return;
  }
  const tiers = getWarrantyTierDocs(job);
  const t = tiers[tierKey];
  if (!t) return;
  triggerDummyDownload(
    t.pdfName,
    t.code + " NATIONAL HOME WARRANTY CERTIFICATE (" + t.badge + ")\nPolicy #" + w.policyNum + "\n" + t.title + "\n" + t.desc,
    t.dataUrl
  );
  showToast("Downloading " + t.pdfName);
}

function openCustomVaultPdfOnScreen(title, pdfName, subtitle, bodyText, dataUrl) {
  const job = getActiveJob();
  const muniName = resolveJobMunicipality(job);
  const titleEl = document.getElementById("pdf-modal-title");
  const bodyEl = document.getElementById("pdf-modal-body");
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (!titleEl || !bodyEl || !dlBtn) return;

  titleEl.innerHTML = `<span>📄</span> ${escapeHtml(title)} &mdash; ${escapeHtml(pdfName)}`;
  dlBtn.onclick = () => triggerDummyDownload(pdfName, title + "\n" + subtitle + "\n" + bodyText, dataUrl || "");

  bodyEl.innerHTML = `
    <div class="kp-pdf-page-sheet">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:14px; margin-bottom:18px;">
        <div>
          <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.1em; text-transform:uppercase; color:#b45309;">KEYSTONE POSSIBILITIES LTD. &bull; VERIFIED PROJECT RECORD</div>
          <h1 style="font-size:1.28rem; font-weight:900; color:#0f172a; margin:4px 0;">${escapeHtml(title)}</h1>
          <div style="font-size:0.84rem; color:#334155; font-weight:600;">${escapeHtml(subtitle)}</div>
        </div>
        <div style="text-align:right; font-size:0.78rem; color:#334155;">
          <div><strong>File:</strong> ${escapeHtml(pdfName)}</div>
          <div><strong>Jurisdiction:</strong> ${escapeHtml(muniName)}</div>
          <div><strong>Permit:</strong> #${escapeHtml(job.permitNum)}</div>
        </div>
      </div>

      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:14px; margin-bottom:18px; font-size:0.84rem; color:#1e293b; line-height:1.6;">
        <div><strong>Project Address:</strong> ${escapeHtml(job.address)} (${escapeHtml(job.jobId)})</div>
        <div><strong>Property Owner(s):</strong> ${escapeHtml(job.ownerName)}</div>
        <div><strong>Licensed Builder:</strong> Keystone Possibilities Ltd. &mdash; Wayne Stevenson (BC #52603)</div>
      </div>

      <h3 style="font-size:0.9rem; font-weight:800; text-transform:uppercase; color:#0f172a; border-bottom:1px solid #cbd5e1; padding-bottom:6px;">Official Document Summary &amp; Technical Record</h3>
      <p style="font-size:0.86rem; line-height:1.65; color:#1e293b; white-space:pre-line;">${escapeHtml(bodyText)}</p>
    </div>
  `;
  openModal("modal-pdf-viewer");
}

function formatActualDateHeading(dateISO) {
  if (!dateISO || !/^\d{4}-\d{2}-\d{2}$/.test(dateISO)) return String(dateISO || "UNDATED RECORD").toUpperCase();
  const parts = dateISO.split("-").map(Number);
  const dt = new Date(parts[0], parts[1] - 1, parts[2]);
  const dows = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"];
  const months = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
  ];
  return dows[dt.getDay()] + ", " + months[dt.getMonth()] + " " + parts[2] + ", " + parts[0];
}

function formatShortActualDate(dateISO) {
  if (!dateISO || !/^\d{4}-\d{2}-\d{2}$/.test(dateISO)) return String(dateISO || "");
  const parts = dateISO.split("-").map(Number);
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return months[(parts[1] - 1) % 12] + " " + parts[2] + ", " + parts[0];
}

function ensureJobDatedVaultDocs(job) {
  const muniName = resolveJobMunicipality(job);
  if (job.datedVaultDocs && job.datedVaultDocs.city && job.datedVaultDocs.eng && job.datedVaultDocs.arch) {
    return job.datedVaultDocs;
  }

  const psArch = (job.planSets && job.planSets.arch) || {
    firm: "Studio Vance Architecture AIBC",
    rev: "Rev 3 (IFC)",
    pdfName: job.jobId + "_Architectural_IFC_Full_Set.pdf",
    dataUrl: ""
  };
  const psEng = (job.planSets && job.planSets.eng) || {
    firm: "Apex Structural P.Eng. & Thurber Geotechnical",
    rev: "Schedule B Sealed",
    pdfName: job.jobId + "_Structural_Geotech_Engineering_Sealed.pdf",
    dataUrl: ""
  };
  const psCity = (job.planSets && job.planSets.city) || {
    firm: muniName + " Building Dept",
    rev: "Permit #" + job.permitNum,
    pdfName: job.jobId + "_City_Approved_Stamped_Permit_Plans.pdf",
    dataUrl: ""
  };

  // Build City Inspections & Permit Plans from job.inspections (Passed/Completed + Active) + Permit Plans
  const cityDocs = [
    {
      id: "city-insp-06",
      dateISO: "2026-10-14",
      code: "PASSED • STAGE 06",
      title: "Structural Steel Moment Frame & High-Strength Bolt Torque Inspection",
      sub: "Apex Structural P.Eng. & " + muniName + " • Zero deficiencies; crane steel moment connections & CWB welds approved",
      pdfName: "INSP-06_Structural_Steel_Moment_Frame.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-10-14\nAuthority: Apex Structural P.Eng. & " + muniName + "\nField Notes: W12x65 wide-flange steel beams, HSS columns, CWB field welds, and base-plate non-shrink grout verified and passed.",
      dataUrl: ""
    },
    {
      id: "city-insp-05",
      dateISO: "2026-09-28",
      code: "PASSED • STAGE 05",
      title: "Dampproofing Membrane, Dimple Mat & Perimeter Weeping Tile Inspection",
      sub: muniName + " Building Inspector • Pre-backfill drainage & washed crush cover approved",
      pdfName: "INSP-05_Dampproofing_DrainTile_Pass.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-09-28\nAuthority: " + muniName + " Building Inspector\nField Notes: 2-coat elastomeric membrane, dimple drainage mat, 4\" PVC perforated drain tile, and filter cloth verified prior to structural backfill.",
      dataUrl: ""
    },
    {
      id: "city-insp-04",
      dateISO: "2026-09-18",
      code: "PASSED • STAGE 04",
      title: "Under-Slab Hydronic, Plumbing DWV Pressure Test & Radon Sub-Slab",
      sub: muniName + " Plumbing & Mechanical Inspector • 10 ft head DWV & radon rock bed passed",
      pdfName: "INSP-04_UnderSlab_Plumbing_Radon.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-09-18\nAuthority: " + muniName + " Plumbing Inspector\nField Notes: Under-slab DWV pressure test passed; 10 mil poly vapor barrier, EPS sub-slab insulation, and passive radon vent pipe certified.",
      dataUrl: ""
    },
    {
      id: "city-insp-03",
      dateISO: "2026-09-09",
      code: "PASSED • STAGE 03",
      title: "Footing & Foundation Wall Rebar Placement (Pre-Pour P.Eng. Review)",
      sub: "Apex Structural P.Eng. & " + muniName + " • 15M/20M epoxy & black bar spacing verified",
      pdfName: "INSP-03_Footing_Wall_Rebar_PrePour.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-09-09\nAuthority: Apex Structural P.Eng. & " + muniName + "\nField Notes: Continuous strip footing and 10\" foundation wall reinforcing steel verified to Sheet S-101 prior to 35 MPa concrete placement.",
      dataUrl: ""
    },
    {
      id: "city-insp-02",
      dateISO: "2026-08-28",
      code: "PASSED • STAGE 02",
      title: "35 MPa Concrete Formwork, Anchor Bolts & Hold-Down Hardware",
      sub: "Apex Structural P.Eng. (Schedule B) • Simpson PAB anchor rods & seismic hold-downs passed",
      pdfName: "INSP-02_Formwork_AnchorBolt_Verification.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-08-28\nAuthority: Apex Structural P.Eng. (Schedule B)\nField Notes: Form alignment, Simpson Strong-Tie PAB anchor bolts, and HDU8 hold-down templates verified.",
      dataUrl: ""
    },
    {
      id: "city-insp-01",
      dateISO: "2026-08-24",
      code: "PASSED • STAGE 01",
      title: "Geotechnical Excavation & Competent Bedrock Bearing Review",
      sub: "Thurber Geotechnical P.Eng. (Schedule B) • Competent granodiorite bedrock verified at 150 kPa+",
      pdfName: "INSP-01_Thurber_Bedrock_Bearing_Report.pdf",
      bodyText: "OFFICIAL PASSED INSPECTION REPORT\nDate: 2026-08-24\nAuthority: Thurber Geotechnical P.Eng.\nField Notes: Excavated subgrade and bedrock bearing capacity verified at >150 kPa allowable pressure; rock dowels approved.",
      dataUrl: ""
    },
    {
      id: "city-permit-plans",
      dateISO: "2026-08-22",
      code: "PERMIT SET",
      title: "City Approved & Red-Stamped Building Permit Plan Set",
      sub: muniName + " Building Dept • Permit #" + job.permitNum + " Full Stamped Drawing Set",
      pdfName: psCity.pdfName,
      bodyText: "Official municipal red-stamped building permit drawing package approved for construction by " + muniName + " under Permit #" + job.permitNum + ".",
      dataUrl: psCity.dataUrl || ""
    },
    {
      id: "city-permit-cert",
      dateISO: "2026-08-22",
      code: "PERMIT #" + job.permitNum,
      title: "Municipal Building Permit Approval & Conditions Certificate",
      sub: muniName + " Chief Building Official • Active Building Permit Authorization",
      pdfName: muniName.replace(/\s+/g, "_") + "_Building_Permit_" + job.permitNum + ".pdf",
      bodyText: "Official Building Permit #" + job.permitNum + " issued by " + muniName + " authorizing full construction at " + job.address + ".",
      dataUrl: ""
    }
  ];

  const engDocs = [
    {
      id: "eng-doc-01",
      dateISO: "2026-10-14",
      code: "FIELD REVIEW",
      title: "Schedule B Structural Field Review — Steel Moment Frame & High-Strength Bolting",
      sub: "Apex Structural Engineering P.Eng. • Signed & Sealed Field Review Memo #04",
      pdfName: job.jobId + "_S-Field_Steel_Moment_Review_2026-10-14.pdf",
      bodyText: "Signed and sealed P.Eng. Schedule B field review confirming structural steel W-beams, HSS columns, and moment welds conform to IFC drawings.",
      dataUrl: ""
    },
    {
      id: "eng-doc-02",
      dateISO: "2026-10-05",
      code: "SHEET S-201",
      title: "Main & Upper Level Framing Plan, Glulam Beams & Simpson Strong-Tie ATS Shear",
      sub: "Apex Structural Engineering P.Eng. • Rev 3 Sealed Structural Framing Sheet",
      pdfName: job.jobId + "_S-201_Framing_Glulam_Simpson_ATS.pdf",
      bodyText: "Engineered TJI 360 floor joist layout, Douglas Fir Glulam ridge beams, and Simpson Strong-Tie HDU8/ATS tie-down shearwall schedule.",
      dataUrl: ""
    },
    {
      id: "eng-doc-03",
      dateISO: "2026-09-09",
      code: "SHEET S-101",
      title: "35 MPa Concrete Foundation Plan, Footing Schedule & Epoxy Rebar Details",
      sub: "Apex Structural Engineering P.Eng. • Rev 3 Sealed Foundation & Retaining Wall Plan",
      pdfName: job.jobId + "_S-101_Foundation_Rebar_Schedule.pdf",
      bodyText: "35 MPa reinforced concrete foundation plan, stepped bedrock footings, and seismic reinforcing bar schedule.",
      dataUrl: ""
    },
    {
      id: "eng-doc-04",
      dateISO: "2026-08-24",
      code: "SHEET G-101",
      title: "Geotechnical Bedrock Bearing Assessment & Epoxied Rock Dowel Schedule",
      sub: "Thurber Geotechnical Engineering P.Eng. • Schedule B Geotechnical Certification",
      pdfName: job.jobId + "_G-101_Geotechnical_Bedrock_Report.pdf",
      bodyText: "Geotechnical investigation, slope stability certification, and Hilti HIT-RE 500 epoxied rock dowel anchorage specifications.",
      dataUrl: ""
    },
    {
      id: "eng-doc-05",
      dateISO: "2026-08-18",
      code: "MASTER SCHEDULE B",
      title: "Complete Sealed Structural, Simpson ATS & Geotechnical Package (All Sheets)",
      sub: psEng.firm + " • Full Sealed Engineering Set & Letters of Assurance",
      pdfName: psEng.pdfName,
      bodyText: "Complete BC Building Code Schedule B sealed structural, geotechnical, civil stormwater ES54, and Step Code 4 mechanical engineering package.",
      dataUrl: psEng.dataUrl || ""
    },
    {
      id: "eng-doc-06",
      dateISO: "2026-08-18",
      code: "SHEET C-101",
      title: "Civil Site Grading, Stormwater Detention Chamber & ES54 Erosion Control",
      sub: "Tantalus Civil Engineering P.Eng. • Municipal Servicing & Drainage Plan",
      pdfName: job.jobId + "_C-101_Civil_Stormwater_ES54.pdf",
      bodyText: "Civil storm/sanitary sewer tie-ins, 100-year stormwater detention tank sizing, and sediment/erosion control plan.",
      dataUrl: ""
    }
  ];

  const archDocs = [
    {
      id: "arch-doc-01",
      dateISO: "2026-10-12",
      code: "SHEET A-202",
      title: "Level 2 Architectural Floor Plan, Vaulted Ceiling & Glulam Canopy Details",
      sub: psArch.firm + " • Issued for Active Stage 09 Upper Level Framing",
      pdfName: job.jobId + "_A-202_Upper_Level_Architectural_Plan.pdf",
      bodyText: "Upper level bedroom suites, vaulted Douglas Fir soffit framing dimensions, and acoustic partition wall assemblies.",
      dataUrl: ""
    },
    {
      id: "arch-doc-02",
      dateISO: "2026-10-01",
      code: "SHEET A-201",
      title: "Main Level Architectural Floor Plan, Window Schedule & Door Openings",
      sub: psArch.firm + " • Rev 3 (IFC) Main Floor Dimensioned Layout",
      pdfName: job.jobId + "_A-201_Main_Level_Architectural_Plan.pdf",
      bodyText: "Main level open-concept architectural layout, triple-pane glazing rough openings, and shearwall gridlines.",
      dataUrl: ""
    },
    {
      id: "arch-doc-03",
      dateISO: "2026-09-14",
      code: "SHEET A-301",
      title: "Exterior Elevations (North, South, East, West) & Rainscreen Cladding",
      sub: psArch.firm + " • Architectural basalt stone, cedar soffit & metal panel details",
      pdfName: job.jobId + "_A-301_Exterior_Elevations_Rainscreen.pdf",
      bodyText: "Full four-sided exterior architectural elevations, geodetic roof ridge height calculations, and rainscreen cladding transitions.",
      dataUrl: ""
    },
    {
      id: "arch-doc-04",
      dateISO: "2026-08-29",
      code: "SHEET A-302",
      title: "Full Building Sections, Stair Geometry & BC Energy Step Code 4 Wall Assemblies",
      sub: psArch.firm + " • R-22 Cavity + R-10 Exterior Rockwool Continuous Insulation",
      pdfName: job.jobId + "_A-302_Sections_StepCode4_Assemblies.pdf",
      bodyText: "Cross-sectional architectural drawings, custom steel/white-oak stair geometry, and air-barrier continuity details.",
      dataUrl: ""
    },
    {
      id: "arch-doc-05",
      dateISO: "2026-08-15",
      code: "MASTER IFC SET",
      title: "Complete Architectural Plan Package (Full IFC Set — Sheets A-101 to A-401)",
      sub: psArch.firm + " • " + psArch.rev + " Complete Stamped Architectural Set",
      pdfName: psArch.pdfName,
      bodyText: "Complete AIBC Issued for Construction architectural drawing set including site plan, floor plans, elevations, sections, and interior millwork schedules.",
      dataUrl: psArch.dataUrl || ""
    },
    {
      id: "arch-doc-06",
      dateISO: "2026-08-15",
      code: "SHEET A-101",
      title: "Architectural Site Plan, Municipal Setbacks, Lot Coverage & Geodetic Benchmarks",
      sub: psArch.firm + " • Verified with BCLS Topographic Survey",
      pdfName: job.jobId + "_A-101_Architectural_Site_Plan.pdf",
      bodyText: "Site layout, front/rear/side yard setback table, driveway grades, and tree protection envelope.",
      dataUrl: ""
    }
  ];

  job.datedVaultDocs = {
    city: cityDocs,
    eng: engDocs,
    arch: archDocs
  };
  return job.datedVaultDocs;
}

function getSortedCategoryDocs(job, catKey) {
  const vault = ensureJobDatedVaultDocs(job);
  const list = (vault[catKey] || []).slice();
  list.sort((a, b) => String(b.dateISO || "").localeCompare(String(a.dateISO || "")));
  return list;
}

function updateVaultDocActualDate(catKey, docId, newDateISO) {
  if (!newDateISO) return;
  const job = getActiveJob();
  const vault = ensureJobDatedVaultDocs(job);
  const list = vault[catKey] || [];
  const item = list.find(d => d.id === docId);
  if (!item) return;
  item.dateISO = newDateISO;
  saveState();
  renderWarrantyAndPlansTab();
  showToast("Updated date to " + formatShortActualDate(newDateISO) + " (re-sorted with most recent at top)");
}

function addDatedVaultEntry(catKey, dateISO, codeBadge, title, subText, pdfName, bodyText, dataUrl) {
  const job = getActiveJob();
  const vault = ensureJobDatedVaultDocs(job);
  const cleanDate = (dateISO && /^\d{4}-\d{2}-\d{2}$/.test(dateISO)) ? dateISO : "2026-10-17";
  const newDoc = {
    id: catKey + "-doc-" + Date.now(),
    dateISO: cleanDate,
    code: codeBadge || "VERIFIED PDF",
    title: title || ("New " + catKey.toUpperCase() + " Document (" + cleanDate + ")"),
    sub: subText || (resolveJobMunicipality(job) + " • Added " + cleanDate),
    pdfName: pdfName || (job.jobId + "_" + catKey.toUpperCase() + "_" + cleanDate + ".pdf"),
    bodyText: bodyText || ("Official project PDF record uploaded on " + cleanDate + " for " + job.address + "."),
    dataUrl: dataUrl || ""
  };
  vault[catKey] = [newDoc].concat(vault[catKey] || []);
  activeP3Discipline = catKey;
  saveState();
  renderWarrantyAndPlansTab();
  showToast("Added to top under " + formatShortActualDate(cleanDate) + ": " + newDoc.pdfName);
  return newDoc;
}

// Expose global hook so Antigravity can automatically push dated PDFs for any job
window.kpAgentAddDatedPdf = addDatedVaultEntry;

function handleDatedVaultPdfUpload(catKey, event) {
  const file = event && event.target && event.target.files && event.target.files[0];
  if (!file) return;
  const dateInput = document.getElementById("p3-new-vault-date");
  const titleInput = document.getElementById("p3-new-vault-title");
  const chosenDate = (dateInput && dateInput.value) ? dateInput.value : "2026-10-17";
  const cleanFileTitle = file.name.replace(/\.[^/.]+$/, "").replace(/[_-]+/g, " ");
  const chosenTitle = (titleInput && titleInput.value.trim()) ? titleInput.value.trim() : cleanFileTitle;

  const badgeMap = {
    city: "CITY / INSPECTION PDF",
    eng: "ENGINEER SEALED PDF",
    arch: "ARCHITECT PLAN PDF"
  };
  const subMap = {
    city: resolveJobMunicipality(getActiveJob()) + " • Permit #" + (getActiveJob().permitNum || "BP2026-0419"),
    eng: (getActiveJob().planSets && getActiveJob().planSets.eng ? getActiveJob().planSets.eng.firm : "Structural & Geotech P.Eng."),
    arch: (getActiveJob().planSets && getActiveJob().planSets.arch ? getActiveJob().planSets.arch.firm : "Project Architect AIBC")
  };

  const reader = new FileReader();
  reader.onload = function(e) {
    const dataUrl = e.target.result || "";
    addDatedVaultEntry(
      catKey,
      chosenDate,
      badgeMap[catKey] || "UPLOADED PDF",
      chosenTitle,
      subMap[catKey] + " • Uploaded PDF Record",
      file.name,
      "Uploaded project PDF file (" + file.name + ") dated " + chosenDate + ".",
      dataUrl
    );
    if (titleInput) titleInput.value = "";
  };
  reader.readAsDataURL(file);
}

function addDatedVaultEntryFromBar(catKey) {
  const dateInput = document.getElementById("p3-new-vault-date");
  const titleInput = document.getElementById("p3-new-vault-title");
  const chosenDate = (dateInput && dateInput.value) ? dateInput.value : "2026-10-17";
  let chosenTitle = (titleInput && titleInput.value.trim()) ? titleInput.value.trim() : "";
  if (!chosenTitle) {
    const labelMap = {
      city: "City Inspection / Permit Report title",
      eng: "Engineering Field Review / Plan title",
      arch: "Architectural Plan / Revision title"
    };
    const prompted = prompt("Enter " + (labelMap[catKey] || "Document title") + " for " + formatShortActualDate(chosenDate) + ":", "");
    if (!prompted || !prompted.trim()) return;
    chosenTitle = prompted.trim();
  }
  const job = getActiveJob();
  const safeFile = job.jobId + "_" + chosenDate + "_" + chosenTitle.replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 42) + ".pdf";
  const badgeMap = {
    city: "PASSED INSPECTION",
    eng: "P.ENG. FIELD REVIEW",
    arch: "ARCHITECT REVISION"
  };
  const subMap = {
    city: resolveJobMunicipality(job) + " • Permit #" + (job.permitNum || "BP2026-0419"),
    eng: (job.planSets && job.planSets.eng ? job.planSets.eng.firm : "Apex Structural P.Eng."),
    arch: (job.planSets && job.planSets.arch ? job.planSets.arch.firm : "Studio Vance Architecture AIBC")
  };
  addDatedVaultEntry(
    catKey,
    chosenDate,
    badgeMap[catKey] || "VERIFIED PDF",
    chosenTitle,
    subMap[catKey] + " • Verified Record",
    safeFile,
    chosenTitle + " — Official dated record (" + chosenDate + ") for " + job.address + ".",
    ""
  );
  if (titleInput) titleInput.value = "";
}

function selectP3DisciplineBox(key) {
  activeP3Discipline = key;
  renderWarrantyAndPlansTab();
}

function renderWarrantyAndPlansTab() {
  const job = getActiveJob();
  const w = job.warranty || {};
  const muniName = resolveJobMunicipality(job);
  const tiers = getWarrantyTierDocs(job);
  ensureJobDatedVaultDocs(job);

  const polBadge = document.getElementById("p3-warranty-policy-badge");
  if (polBadge) polBadge.innerText = "POLICY #" + (w.policyNum || "NHW-2026-88421");

  const permBadge = document.getElementById("p3-plans-permit-badge");
  if (permBadge) permBadge.innerText = muniName + " • Permit #" + (job.permitNum || "BP2026-0419");

  // 1. Render 3 Warranty Tier Boxes (Each with Open PDF & Download PDF right inside the box)
  const tiersGrid = document.getElementById("p3-warranty-tiers-grid");
  if (tiersGrid) {
    tiersGrid.innerHTML = ["2yr", "5yr", "10yr"].map(k => {
      const t = tiers[k];
      return `
        <div class="kp-pdf-master-card" style="cursor:default;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:8px;">
              <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.18rem; font-weight:900; color:#d4af37;">${escapeHtml(t.code)}</span>
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(t.badge)}</span>
            </div>
            <div style="font-size:0.86rem; font-weight:800; color:#ffffff; margin-bottom:5px; line-height:1.3;">
              ${escapeHtml(t.title)}
            </div>
            <div style="font-size:0.74rem; color:#cbd5e1; line-height:1.45; margin-bottom:9px;">
              ${escapeHtml(t.desc)}
            </div>
            <div class="kp-pdf-file-pill" title="${escapeHtml(t.pdfName)}" style="margin-bottom:8px;">
              PDF: ${escapeHtml(t.pdfName)}
            </div>
          </div>
          <div class="kp-pdf-btn-row">
            <button type="button" onclick="openWarrantyTierPdfOnScreen('${k}')" class="kp-gold-btn kp-pill-sm" style="flex:1; justify-content:center;">
              Open PDF
            </button>
            <button type="button" onclick="downloadWarrantyTierPdf('${k}')" class="kp-secondary-btn kp-pill-sm" style="flex:1; justify-content:center;">
              Download PDF
            </button>
          </div>
        </div>
      `;
    }).join("");
  }

  const metaBar = document.getElementById("p3-warranty-meta-bar");
  if (metaBar) {
    metaBar.innerHTML = `
      <div><strong style="color:#ffffff;">Warranty Provider:</strong> ${escapeHtml(w.provider)} &bull; <strong style="color:#ffffff;">Builder:</strong> ${escapeHtml(w.builderLicense)}</div>
      <div><strong style="color:#ffffff;">Master Certificate:</strong> <span style="color:#f3e5ab;">${escapeHtml(w.pdfName)}</span> &bull; <strong style="color:#ffffff;">Status:</strong> <span style="color:#d4af37;">${escapeHtml(w.status)}</span></div>
    `;
  }

  // 2. Render 3 Clickable Discipline Boxes (Pick between City Inspections, Engineer, and Architect)
  const pGrid = document.getElementById("p3-plan-disciplines-grid");
  const cityDocs = getSortedCategoryDocs(job, "city");
  const engDocs = getSortedCategoryDocs(job, "eng");
  const archDocs = getSortedCategoryDocs(job, "arch");

  if (pGrid) {
    const cards = [
      {
        key: "city",
        badge: "1. CITY INSPECTIONS & PLANS",
        latestDate: cityDocs.length ? ("Latest: " + formatShortActualDate(cityDocs[0].dateISO)) : "No Dates Yet",
        countBadge: cityDocs.length + " Dated PDFs",
        title: "City Inspections & Approved Plans",
        sub: muniName + " • Permit #" + job.permitNum,
        desc: "Most recent passed municipal inspections at top + red-stamped city permit plans, sectioned by actual job dates."
      },
      {
        key: "eng",
        badge: "2. ENGINEER PLANS & REVIEWS",
        latestDate: engDocs.length ? ("Latest: " + formatShortActualDate(engDocs[0].dateISO)) : "No Dates Yet",
        countBadge: engDocs.length + " Dated PDFs",
        title: "Engineer Plans & Field Reviews",
        sub: job.planSets.eng.firm + " • Schedule B Sealed",
        desc: "Most recent P.Eng. Schedule B field inspections at top + structural, rebar, Simpson ATS & geotech PDFs by date."
      },
      {
        key: "arch",
        badge: "3. ARCHITECT PLANS & REVISIONS",
        latestDate: archDocs.length ? ("Latest: " + formatShortActualDate(archDocs[0].dateISO)) : "No Dates Yet",
        countBadge: archDocs.length + " Dated PDFs",
        title: "Architect Plans (AIBC IFC Set)",
        sub: job.planSets.arch.firm + " • " + job.planSets.arch.rev,
        desc: "Most recent architectural floor plans, elevations, Step Code 4 assemblies & revisions at top, sectioned by actual date."
      }
    ];

    pGrid.innerHTML = cards.map(c => {
      const isAct = (activeP3Discipline === c.key);
      return `
        <div
          class="kp-pdf-master-card"
          onclick="selectP3DisciplineBox('${c.key}')"
          style="border-color:${isAct ? "#d4af37" : "rgba(255,255,255,0.16)"} !important; background:${isAct ? "linear-gradient(180deg, rgba(212,175,55,0.10) 0%, #0b0f17 100%)" : "#0b0f17"} !important; box-shadow:${isAct ? "0 0 18px rgba(212,175,55,0.22)" : "none"} !important;"
        >
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:7px; flex-wrap:wrap;">
              <span class="kp-badge-pill ${isAct ? "kp-badge-gold" : "kp-badge-white"}">${escapeHtml(c.badge)}</span>
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(c.latestDate)} &bull; ${escapeHtml(c.countBadge)}</span>
            </div>
            <div style="font-size:0.9rem; font-weight:900; color:#ffffff; line-height:1.3;">${escapeHtml(c.title)}</div>
            <div style="font-size:0.73rem; color:#f3e5ab; font-weight:700; margin:4px 0;">${escapeHtml(c.sub)}</div>
            <div style="font-size:0.73rem; color:#cbd5e1; line-height:1.4;">${escapeHtml(c.desc)}</div>
          </div>
          <div class="kp-pdf-btn-row" style="margin-top:6px;">
            <button type="button" onclick="event.stopPropagation(); selectP3DisciplineBox('${c.key}')" class="${isAct ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm" style="flex:1; justify-content:center;">
              ${isAct ? "Viewing Dated PDFs Below" : "Click to Open Dated PDFs"}
            </button>
            <button type="button" onclick="event.stopPropagation(); downloadPlanSetPdf('${c.key}')" class="kp-secondary-btn kp-pill-sm" title="Download Master PDF">
              Master PDF
            </button>
          </div>
        </div>
      `;
    }).join("");
  }

  // Render the Scrollable Dated White-on-Black PDF Vault Drawer (Most Recent at Top)
  renderDisciplineFilesVault();

  // 3. Render Pre-Occupancy Final Walkthrough & Dual 2-5-10 Sign-Off at Bottom
  const ownerNameEl = document.getElementById("p3-owner-signoff-name");
  if (ownerNameEl) ownerNameEl.innerText = job.ownerName || "David & Sarah Kensington";

  const statusPill = document.getElementById("p3-walkthrough-status-pill");
  const wtStatus = document.getElementById("p3-walkthrough-signoff-status");
  const btnSign = document.getElementById("p3-btn-dual-signoff");

  if (job.walkthroughSigned) {
    if (statusPill) {
      statusPill.className = "kp-badge-pill kp-badge-gold";
      statusPill.innerText = "✓ Dual Signed & 2-5-10 Activated (" + job.walkthroughSignedDate + ")";
    }
    if (wtStatus) {
      wtStatus.innerHTML = `<span style="color:#f3e5ab; font-weight:700;">&#10003; Co-Signed by ${escapeHtml(job.ownerName)} &amp; Wayne Stevenson (#52603) on ${escapeHtml(job.walkthroughSignedDate)}</span>`;
    }
    if (btnSign) {
      btnSign.innerText = "✓ 2-5-10 & Walkthrough Signed by Both Parties";
    }
  } else {
    if (statusPill) {
      statusPill.className = "kp-badge-pill kp-badge-white";
      statusPill.innerText = "Awaiting Final Walkthrough Sign-Off";
    }
    if (wtStatus) {
      wtStatus.innerText = "Ready for Owner & Builder 2-5-10 Co-Sign-Off";
    }
    if (btnSign) {
      btnSign.innerText = "Sign Off 2-5-10 & Final Walkthrough (Both Parties)";
    }
  }

  const bottomPdfBar = document.getElementById("p3-bottom-walkthrough-pdf-bar");
  if (bottomPdfBar) {
    const pdfFile = job.walkthroughPdfName || (job.jobId + "_Final_Walkthrough_and_2-5-10_Certificate_Signed.pdf");
    bottomPdfBar.innerHTML = `
      <div style="display:flex; align-items:center; gap:10px; min-width:0; flex-wrap:wrap;">
        <span class="kp-badge-pill kp-badge-gold">FINAL WALKTHROUGH &amp; 2-5-10 PDF</span>
        <span style="font-size:0.82rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
          ${escapeHtml(pdfFile)}
        </span>
        <span style="font-size:0.73rem; color:#cbd5e1;">
          &bull; ${job.walkthroughSigned ? "Dual Signed by Wayne Stevenson (#52603) & " + escapeHtml(job.ownerName) : "Pre-Occupancy Walkthrough & 2-5-10 Sign-Off Package"}
        </span>
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <button type="button" onclick="openWalkthroughPdfOnScreen()" class="kp-gold-btn kp-pill-sm">
          Open PDF on Screen
        </button>
        <button type="button" onclick="downloadWalkthroughReportPdf()" class="kp-secondary-btn kp-pill-sm">
          Download PDF
        </button>
      </div>
    `;
  }
}

function renderDisciplineFilesVault() {
  const job = getActiveJob();
  const muniName = resolveJobMunicipality(job);
  const drawer = document.getElementById("p3-discipline-files-drawer");
  if (!drawer) return;

  const catKey = activeP3Discipline || "city";
  const sortedDocs = getSortedCategoryDocs(job, catKey);

  // Group sortedDocs by actual dateISO (preserving Newest -> Oldest order)
  const dateGroups = [];
  const groupMap = {};
  sortedDocs.forEach(doc => {
    const dKey = doc.dateISO || "2026-10-15";
    if (!groupMap[dKey]) {
      groupMap[dKey] = { dateISO: dKey, items: [] };
      dateGroups.push(groupMap[dKey]);
    }
    groupMap[dKey].items.push(doc);
  });

  const catMeta = {
    city: {
      title: "CITY INSPECTIONS & APPROVED PERMIT PLANS",
      sub: muniName + " • Permit #" + (job.permitNum || "BP2026-0419"),
      uploadBtn: "+ Upload City / Inspection PDF"
    },
    eng: {
      title: "ENGINEER PLANS & SCHEDULE B FIELD REVIEWS",
      sub: (job.planSets && job.planSets.eng ? job.planSets.eng.firm : "Apex Structural P.Eng.") + " • Sealed Schedule B",
      uploadBtn: "+ Upload Engineer PDF"
    },
    arch: {
      title: "ARCHITECTURAL PLANS & REVISIONS (AIBC IFC)",
      sub: (job.planSets && job.planSets.arch ? job.planSets.arch.firm : "Studio Vance Architecture AIBC") + " • " + (job.planSets && job.planSets.arch ? job.planSets.arch.rev : "Rev 3 IFC"),
      uploadBtn: "+ Upload Architect PDF"
    }
  }[catKey];

  const defaultTodayISO = job.whereWeAreDate || "2026-10-17";

  drawer.innerHTML = `
    <!-- Top Category Switcher & Auto-Dated Upload Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-bottom:10px; margin-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.14);">
      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <button type="button" onclick="selectP3DisciplineBox('city')" class="${catKey === "city" ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm">
          1. City Inspections (${getSortedCategoryDocs(job, "city").length})
        </button>
        <button type="button" onclick="selectP3DisciplineBox('eng')" class="${catKey === "eng" ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm">
          2. Engineer (${getSortedCategoryDocs(job, "eng").length})
        </button>
        <button type="button" onclick="selectP3DisciplineBox('arch')" class="${catKey === "arch" ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm">
          3. Architect (${getSortedCategoryDocs(job, "arch").length})
        </button>
        <span style="font-size:0.8rem; font-weight:800; color:#ffffff; margin-left:4px;">
          ${escapeHtml(catMeta.sub)}
        </span>
      </div>

      <!-- Auto-Dated Upload / Add Entry Controls (Automatically Puts Newest Date at Top) -->
      <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap; background:#0b0f17; border:1px solid rgba(255,255,255,0.18); border-radius:9999px; padding:4px 10px;">
        <span style="font-size:0.67rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.05em;">Actual Date:</span>
        <input
          type="date"
          id="p3-new-vault-date"
          value="${escapeHtml(defaultTodayISO)}"
          class="kp-inline-date-edit"
          title="Pick Actual Date for New Upload or Entry"
        />
        <input
          type="text"
          id="p3-new-vault-title"
          placeholder="Optional title (or upload PDF)..."
          style="background:#05070b !important; border:1px solid rgba(255,255,255,0.2) !important; color:#ffffff !important; border-radius:9999px !important; padding:4px 11px !important; font-size:0.73rem !important; width:195px !important; height:28px !important; margin:0 !important; outline:none !important;"
          onkeydown="if(event.key==='Enter') addDatedVaultEntryFromBar('${catKey}')"
        />
        <button type="button" onclick="addDatedVaultEntryFromBar('${catKey}')" class="kp-secondary-btn kp-pill-sm">
          + Add Entry
        </button>
        <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer; margin:0;">
          ${escapeHtml(catMeta.uploadBtn)}
          <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleDatedVaultPdfUpload('${catKey}', event)" />
        </label>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:9px; font-size:0.72rem; color:#cbd5e1;">
      <div>
        <strong style="color:#d4af37;">SORTED MOST RECENT AT TOP:</strong> Sectioned by actual job dates &mdash; scroll inside the box below to view earlier dates.
      </div>
      <div>
        Change any date on the right of a file to match the current job schedule (auto-sorts immediately).
      </div>
    </div>

    <!-- Scrollable Dated Sections Container (Most Recent Date Section at the Very Top) -->
    <div class="kp-dated-vault-scroll" id="p3-dated-vault-scroll">
      ${dateGroups.map((grp, grpIdx) => {
        const isNewest = (grpIdx === 0);
        return `
          <div class="kp-date-section-block ${isNewest ? "most-recent-date" : ""}">
            <div class="kp-date-section-header">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill ${isNewest ? "kp-badge-gold" : "kp-badge-white"}">
                  ${escapeHtml(formatActualDateHeading(grp.dateISO))}
                </span>
                ${isNewest ? `<span class="kp-badge-pill kp-badge-gold" style="background:rgba(212,175,55,0.22); color:#f3e5ab;">MOST RECENT</span>` : ""}
              </div>
              <span style="font-size:0.69rem; font-weight:800; color:#94a3b8; text-transform:uppercase; letter-spacing:0.06em;">
                ${grp.items.length} ${grp.items.length === 1 ? "PDF Record" : "PDF Records"} &bull; ${escapeHtml(grp.dateISO)}
              </span>
            </div>

            <div style="display:flex; flex-direction:column; gap:7px;">
              ${grp.items.map(doc => `
                <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.16); border-radius:9px; padding:9px 13px; display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
                  <div style="min-width:0; flex:1;">
                    <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                      <span style="background:#05070b; border:1px solid rgba(255,255,255,0.28); color:#ffffff; font-size:0.66rem; font-weight:900; padding:2px 8px; border-radius:9999px;">
                        ${escapeHtml(doc.code)}
                      </span>
                      <span style="font-size:0.82rem; font-weight:800; color:#ffffff;">
                        ${escapeHtml(doc.title)}
                      </span>
                    </div>
                    <div style="font-size:0.72rem; color:#cbd5e1; margin-top:3px;">
                      ${escapeHtml(doc.sub)} &bull; <span style="color:#ffffff; font-weight:700;">${escapeHtml(doc.pdfName)}</span>
                    </div>
                  </div>

                  <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">
                    <input
                      type="date"
                      value="${escapeHtml(doc.dateISO)}"
                      onchange="updateVaultDocActualDate('${catKey}', '${escapeHtml(doc.id)}', this.value)"
                      class="kp-inline-date-edit"
                      title="Change actual date for this job (automatically re-sorts)"
                    />
                    <button
                      type="button"
                      onclick="openCustomVaultPdfOnScreen('${escapeHtml(doc.title.replace(/'/g, "\\'"))}', '${escapeHtml(doc.pdfName.replace(/'/g, "\\'"))}', '${escapeHtml(( formatShortActualDate(doc.dateISO) + " • " + doc.sub ).replace(/'/g, "\\'"))}', '${escapeHtml((doc.bodyText || "").replace(/'/g, "\\'"))}', '${doc.dataUrl || ""}')"
                      class="kp-secondary-btn kp-pill-sm"
                    >
                      Open PDF
                    </button>
                    <button
                      type="button"
                      onclick="triggerDummyDownload('${escapeHtml(doc.pdfName.replace(/'/g, "\\'"))}', '${escapeHtml((doc.title + " (" + doc.dateISO + ") - " + doc.sub + "\n" + (doc.bodyText || "")).replace(/'/g, "\\'"))}', '${doc.dataUrl || ""}')"
                      class="kp-gold-btn kp-pill-sm"
                    >
                      Download PDF
                    </button>
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        `;
      }).join("")}
    </div>
  `;
}

function openWalkthroughPdfOnScreen() {
  const job = getActiveJob();
  const pdfFile = job.walkthroughPdfName || (job.jobId + "_Final_Walkthrough_and_2-5-10_Certificate_Signed.pdf");
  const statusText = job.walkthroughSigned
    ? "DUAL SIGNED & CERTIFIED by Wayne Stevenson (BC Licensed Builder #52603) and " + job.ownerName + " on " + job.walkthroughSignedDate
    : "Pre-Occupancy Final Walkthrough & 2-5-10 Warranty Commencement Certificate";
  const checklistLines = (job.walkthrough || []).map(w => "• " + w.area + ": " + w.item + " [VERIFIED]").join("\n");
  openCustomVaultPdfOnScreen(
    "Pre-Occupancy Final Walkthrough & 2-5-10 Warranty Sign-Off Certificate",
    pdfFile,
    statusText,
    "This official Pre-Occupancy Final Walkthrough & Certificate of Possession confirms completion of quality inspection checkpoints between Keystone Possibilities Ltd. (Wayne Stevenson, BC Builder #52603) and Property Owner(s) " + job.ownerName + " for " + job.address + ", activating the 2-5-10 Year National Home Warranty (Policy #" + job.warranty.policyNum + ").\n\n" + checklistLines,
    job.walkthroughPdfDataUrl || ""
  );
}


function handleWarrantyPdfUpload(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.warranty.pdfName = file.name;
    job.warranty.pdfDataUrl = e.target.result;
    saveState();
    renderWarrantyAndPlansTab();
    showToast("📤 Uploaded 2-5-10 Warranty PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadWarrantyCertificatePdf() {
  const job = getActiveJob();
  const w = job.warranty;
  triggerDummyDownload(w.pdfName, "2-5-10 National Home Warranty Policy #" + w.policyNum + " for " + job.address, w.pdfDataUrl);
}

function promptEditWarrantyDetails() {
  const job = getActiveJob();
  const pol = prompt("Enter 2-5-10 National Home Warranty Policy Number:", job.warranty.policyNum);
  if (!pol) return;
  job.warranty.policyNum = pol;
  saveState();
  renderWarrantyAndPlansTab();
}

function handlePlanSetPdfUpload(key, ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.planSets[key].pdfName = file.name;
    job.planSets[key].date = new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" });
    job.planSets[key].dataUrl = e.target.result;
    saveState();
    renderWarrantyAndPlansTab();
    showToast("📤 Uploaded " + job.planSets[key].discipline + ": " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadPlanSetPdf(key) {
  const job = getActiveJob();
  const ps = job.planSets[key];
  if (!ps) return;
  triggerDummyDownload(ps.pdfName, ps.discipline + " — " + ps.firm + " (" + ps.rev + ")", ps.dataUrl);
  showToast("📥 Downloading " + ps.pdfName);
}

function toggleCadViewerCollapse() {
  const el = document.getElementById("p3-cad-viewer-wrapper");
  if (!el) return;
  el.style.display = (el.style.display === "none") ? "grid" : "none";
}

function updateInspectionDate(idx, val) {
  const job = getActiveJob();
  if (job.inspections[idx]) {
    job.inspections[idx].date = val;
    saveState();
    renderCalendar();
    showToast("📅 Synced Inspection Date to Live Calendar: " + val);
  }
}

function updateInspectionStatus(idx, val) {
  const job = getActiveJob();
  if (job.inspections[idx]) {
    job.inspections[idx].status = val;
    saveState();
    showToast("Updated Inspection Status to " + val);
  }
}

function handleInspectionPdfUpload(idx, ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.inspections[idx].pdfName = file.name;
    job.inspections[idx].pdfDataUrl = e.target.result;
    saveState();
    renderWarrantyAndPlansTab();
    showToast("📤 Uploaded Inspection Report PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadInspectionPdf(idx) {
  const job = getActiveJob();
  const ins = job.inspections[idx];
  if (!ins) return;
  triggerDummyDownload(ins.pdfName, "Inspection Report: " + ins.title + " | Status: " + ins.status + " | " + ins.notes, ins.pdfDataUrl);
}

function addInspectionRowModal() {
  const job = getActiveJob();
  const title = prompt("Enter Inspection Title (e.g. Pre-Pour Garage Slab Inspection):");
  if (!title) return;
  const auth = prompt("Enter Inspector / Authority:", job.municipality + " Building Inspector") || job.municipality;
  const date = prompt("Enter Inspection Date (YYYY-MM-DD):", job.whereWeAreDate) || job.whereWeAreDate;
  job.inspections.push({
    id: "INSP-" + (job.inspections.length + 1),
    stage: String(job.inspections.length + 1).padStart(2, "0"),
    title: title,
    authority: auth,
    date: date,
    status: "Scheduled",
    notes: "Scheduled field review.",
    pdfName: "Inspection_Report_" + (job.inspections.length + 1) + ".pdf"
  });
  saveState();
  renderWarrantyAndPlansTab();
  renderCalendar();
}

function toggleWalkthroughItem(idx) {
  const job = getActiveJob();
  if (job.walkthrough[idx]) {
    job.walkthrough[idx].done = !job.walkthrough[idx].done;
    saveState();
    renderWarrantyAndPlansTab();
  }
}

function addWalkthroughItemPrompt() {
  const job = getActiveJob();
  const area = prompt("Enter Room / Area (e.g. 13. Rooftop Hot Tub & Cedar Deck):");
  if (!area) return;
  const item = prompt("Enter Quality Inspection Item:") || "Verified complete and deficiency-free";
  job.walkthrough.push({ id: Date.now(), area: area, item: item, done: false });
  saveState();
  renderWarrantyAndPlansTab();
}

function handleWalkthroughPdfUpload(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const reader = new FileReader();
  reader.onload = function(e) {
    job.walkthroughPdfName = file.name;
    job.walkthroughPdfDataUrl = e.target.result;
    saveState();
    renderWarrantyAndPlansTab();
    showToast("📤 Uploaded Walkthrough PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function downloadWalkthroughReportPdf() {
  const job = getActiveJob();
  const lines = (job.walkthrough || []).map(w => `[${w.done ? "PASS" : "OPEN"}] ${w.area}: ${w.item}`).join("\r\n");
  triggerDummyDownload(job.walkthroughPdfName, "PRE-OCCUPANCY WALKTHROUGH REPORT\r\n" + lines, job.walkthroughPdfDataUrl);
}

function signOffFinalWalkthrough() {
  const job = getActiveJob();
  const signer = prompt("Enter Property Owner Full Name to Sign Off Pre-Occupancy Walkthrough & Activate 2-5-10 Warranty:", job.ownerName);
  if (!signer) return;
  (job.walkthrough || []).forEach(w => { w.done = true; });
  job.walkthroughSigned = true;
  job.walkthroughSignedDate = new Date().toLocaleDateString("en-US", { month: "short", day: "2-digit", year: "numeric" });
  saveState();
  renderWarrantyAndPlansTab();
  showToast("✅ Final Pre-Occupancy Walkthrough Signed Off & 2-5-10 Warranty Activated!");
}

// Interactive 13-Sheet Vector CAD Blueprint Viewer
const blueprintSheets = {
  arch: [
    { id: "A-101", title: "Site Plan & Building Placement", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Property setbacks, driveway grades, civil hookups, environmental 15m buffer." },
    { id: "A-102", title: "Foundation & Lower Level Layout", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Grade beams, elevator pit, mechanical room, storage suites, perimeter drainage." },
    { id: "A-103", title: "Main Floor Architectural Plan", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Open living concept, chef's kitchen islands, STC 55 acoustic party walls." },
    { id: "A-104", title: "Upper Floor Plan & Roof Terrace", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Primary suites, outdoor living terraces, waterproofing details." },
    { id: "A-201", title: "Exterior Elevations (North, South, East, West)", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Standing seam metal, clear cedar rainscreen, triple-pane window schedules." },
    { id: "A-301", title: "Wall Assemblies & Step Code 4 Envelope", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "2x6 framing, SIGA Majvest/Majrex continuous air barriers, Gutex wood fiber." },
    { id: "A-401", title: "Interior Architectural Millwork & Stairs", rev: "Rev 3 (IFC)", date: "Aug 15, 2026", desc: "Rift-sawn white oak cabinetry, floating timber treads, glass balustrades." }
  ],
  eng: [
    { id: "S-101", title: "Structural Shear Walls & Simpson ATS Schedules", rev: "Rev 3 (IFC)", date: "Aug 18, 2026", desc: "Continuous tie-down holdown rod systems, take-up devices, shear ply nailing." },
    { id: "S-102", title: "Foundation Rebar & 35 MPa Grade Beam Details", rev: "Rev 3 (IFC)", date: "Aug 18, 2026", desc: "15M/20M steel reinforcing bar placement, slab dowels, bedrock anchor ties." },
    { id: "C-101", title: "Civil BC Hydro ES54 Underground Duct Banks & PMT Pad", rev: "Rev 3 (IFC)", date: "Aug 20, 2026", desc: "4-inch rigid PVC ducts, concrete PMT transformer pad, pull vaults." },
    { id: "C-102", title: "Civil Stormwater Retention & Sanitary Servicing", rev: "Rev 3 (IFC)", date: "Aug 20, 2026", desc: "Storm retention tank, oil-grit separator, municipal gravity tie-in." },
    { id: "M-101", title: "Mechanical Zehnder ComfoAir HRV & Heat Pump Schematics", rev: "Rev 3 (IFC)", date: "Aug 22, 2026", desc: "Dedicated fresh air supply/exhaust duct routing, TECA balanced airflow." },
    { id: "E-101", title: "Electrical 400A Three-Phase Switchgear & EV Panels", rev: "Rev 3 (IFC)", date: "Aug 22, 2026", desc: "400A service entrance, smart load management, dual Level 2 EV circuits." }
  ]
};
let activeBlueprintCat = "arch";
let activeSheetIndex = 0;
let blueprintZoom = 1.0;

function switchBlueprintCategory(cat) {
  activeBlueprintCat = cat;
  activeSheetIndex = 0;
  blueprintZoom = 1.0;
  const btnArch = document.getElementById("btn-cat-arch");
  const btnEng = document.getElementById("btn-cat-eng");
  if (btnArch && btnEng) {
    btnArch.style.background = cat === "arch" ? "#d4af37" : "transparent";
    btnArch.style.color = cat === "arch" ? "#04070d" : "#94a3b8";
    btnEng.style.background = cat === "eng" ? "#d4af37" : "transparent";
    btnEng.style.color = cat === "eng" ? "#04070d" : "#94a3b8";
  }
  renderSheetList();
  renderActiveBlueprint();
}

function renderSheetList() {
  const sheets = blueprintSheets[activeBlueprintCat] || [];
  const lbl = document.getElementById("sheet-count-label");
  if (lbl) lbl.innerText = sheets.length + " Sheets";
  const list = document.getElementById("kp-sheet-list");
  if (!list) return;
  list.innerHTML = sheets.map((s, idx) => `
    <div class="kp-sheet-item ${idx === activeSheetIndex ? "active" : ""}" onclick="selectSheet(${idx})">
      <div class="kp-sheet-num"><span>${escapeHtml(s.id)}</span><span style="color:#38bdf8;">${escapeHtml(s.rev)}</span></div>
      <div class="kp-sheet-name">${escapeHtml(s.title)}</div>
      <div class="kp-sheet-desc">${escapeHtml(s.desc)}</div>
    </div>
  `).join("");
}

function selectSheet(idx) {
  activeSheetIndex = idx;
  renderSheetList();
  renderActiveBlueprint();
}

function navigateSheet(dir) {
  const sheets = blueprintSheets[activeBlueprintCat];
  activeSheetIndex = (activeSheetIndex + dir + sheets.length) % sheets.length;
  selectSheet(activeSheetIndex);
}

function changeSheetRevision(rev) {
  blueprintSheets[activeBlueprintCat][activeSheetIndex].rev = rev;
  renderSheetList();
  renderActiveBlueprint();
}

function zoomBlueprint(f) {
  blueprintZoom = Math.min(2.6, Math.max(0.6, blueprintZoom * f));
  const c = document.getElementById("kp-blueprint-container");
  if (c) c.style.transform = `scale(${blueprintZoom})`;
}

function resetBlueprintZoom() {
  blueprintZoom = 1.0;
  const c = document.getElementById("kp-blueprint-container");
  if (c) c.style.transform = "scale(1)";
}

function downloadActiveBlueprintSheet() {
  const s = blueprintSheets[activeBlueprintCat][activeSheetIndex];
  triggerDummyDownload(s.id + "_" + s.title.replace(/[^a-zA-Z0-9]/g, "_") + ".pdf", "CAD Sheet " + s.id + ": " + s.title + " (" + s.desc + ")");
}

function renderActiveBlueprint() {
  const job = getActiveJob();
  const s = blueprintSheets[activeBlueprintCat][activeSheetIndex];
  if (!s) return;
  const idEl = document.getElementById("active-sheet-id");
  if (!idEl) return;
  idEl.innerText = s.id;
  document.getElementById("active-sheet-title").innerText = s.title;
  document.getElementById("active-sheet-rev").innerText = s.rev;
  const isArch = activeBlueprintCat === "arch";
  const strokeColor = isArch ? "#38bdf8" : "#d4af37";
  const c = document.getElementById("kp-blueprint-container");
  if (!c) return;
  c.innerHTML = `
    <svg viewBox="0 0 900 520" width="100%" height="auto" style="background:#020712; border:2px solid ${strokeColor}; border-radius:10px;">
      <defs>
        <pattern id="kpCadGrid" width="36" height="36" patternUnits="userSpaceOnUse">
          <path d="M 36 0 L 0 0 0 36" fill="none" stroke="rgba(56,189,248,0.07)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="900" height="520" fill="url(#kpCadGrid)" />
      <rect x="45" y="38" width="535" height="440" fill="rgba(56,189,248,0.04)" stroke="${strokeColor}" stroke-width="2.5" />
      <rect x="95" y="88" width="435" height="310" fill="rgba(212,175,55,0.06)" stroke="#d4af37" stroke-width="2" stroke-dasharray="6,4" />
      <line x1="312" y1="88" x2="312" y2="398" stroke="#38bdf8" stroke-width="2" />
      <line x1="95" y1="240" x2="530" y2="240" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="4,4" />
      <text x="312" y="68" fill="#ffffff" font-size="14" font-weight="800" text-anchor="middle">${escapeHtml(s.id)} — ${escapeHtml(s.title.toUpperCase())}</text>
      <text x="312" y="175" fill="#f3e5ab" font-size="12" font-weight="700" text-anchor="middle">${escapeHtml(job.address)}</text>
      <text x="312" y="200" fill="#38bdf8" font-size="11" text-anchor="middle">${escapeHtml(s.desc)}</text>
      <text x="312" y="325" fill="#cbd5e1" font-size="11" text-anchor="middle">2x6 Exterior Shear Framing @ 16" O.C. &bull; 35 MPa Concrete &bull; Simpson Strong-Tie ATS</text>
      <text x="312" y="445" fill="#d4af37" font-size="11" font-weight="800" text-anchor="middle">BC ENERGY STEP CODE 4 CERTIFIED &bull; 2-5-10 NATIONAL HOME WARRANTY</text>
      <rect x="600" y="310" width="275" height="170" fill="#070d1b" stroke="#d4af37" stroke-width="2" />
      <text x="737" y="336" fill="#ffffff" font-size="12" font-family="'Outfit','Plus Jakarta Sans',sans-serif" font-weight="900" text-anchor="middle">KEYSTONE POSSIBILITIES LTD.</text>
      <text x="737" y="354" fill="#d4af37" font-size="10" font-weight="800" text-anchor="middle">BC LICENSED BUILDER #52603</text>
      <text x="615" y="380" fill="#38bdf8" font-size="10" font-weight="800">JOB: ${escapeHtml(job.jobId)}</text>
      <text x="615" y="400" fill="#ffffff" font-size="10">OWNER: ${escapeHtml(job.ownerName.slice(0, 26))}</text>
      <text x="615" y="420" fill="#cbd5e1" font-size="10">SHEET: ${escapeHtml(s.id)} (${escapeHtml(s.rev)})</text>
      <text x="615" y="440" fill="#d4af37" font-size="10">SUPERINTENDENT: Wayne Stevenson</text>
      <text x="615" y="460" fill="#38bdf8" font-size="9">PERMIT: ${escapeHtml(job.permitNum)}</text>
    </svg>
  `;
}

// ============================================================================
// 8. TAB 4: 22-STAGE MASTER TRADES BREAKDOWN & TRADE COMMAND MODAL
// ============================================================================

let activeTradeFilter = "ALL";
let activeTradeModalId = null;
let selectedP4TradeId = null;

function ensureArchitectToFinish22Trades(job) {
  if (!job) return;
  const s = (job.contractPrice && job.contractPrice > 2500000) ? (job.contractPrice / 1850000) : 1.0;
  const factory30 = buildFactoryTradesForJob(s, 0);

  if (!Array.isArray(job.trades) || job.trades.length < 30) {
    const oldTrades = Array.isArray(job.trades) ? job.trades : [];
    const customAbove30 = oldTrades.filter(t => Number(t.phase) > 30);
    // Preserve any user-created revisions or signed states by matching trade name or CO id
    const existingRevsByCoId = {};
    oldTrades.forEach(ot => {
      if (Array.isArray(ot.revisions)) {
        ot.revisions.forEach(rv => {
          if (rv && rv.id) existingRevsByCoId[rv.id] = rv;
        });
      }
    });
    factory30.forEach(ft => {
      if (Array.isArray(ft.revisions)) {
        ft.revisions = ft.revisions.map(rv => existingRevsByCoId[rv.id] || rv);
      }
    });
    job.trades = factory30.concat(customAbove30);
  }

  // Normalize contractPdf date and owner signature fields on all 30+ trades
  (job.trades || []).forEach((tr, idx) => {
    if (!tr.id) tr.id = idx + 1;
    tr.phase = String(tr.phase || (idx + 1)).padStart(2, "0");
    if (!tr.sub) tr.sub = tr.trade || "Keystone Assigned Subcontractor";
    if (!tr.contact) tr.contact = "Project Foreman";
    if (!tr.phone) tr.phone = "(604) 848-9688";
    if (!tr.startDate) tr.startDate = "2026-10-15";
    if (!tr.endDate) tr.endDate = "2026-11-15";
    if (typeof tr.contract === "undefined") tr.contract = 35000;
    if (typeof tr.billed === "undefined") tr.billed = 0;
    if (!Array.isArray(tr.revisions)) tr.revisions = [];
    if (!Array.isArray(tr.docs)) tr.docs = [];
    if (!tr.contractPdf || typeof tr.contractPdf !== "object") {
      tr.contractPdf = {
        name: "Stage_" + tr.phase + "_" + String(tr.name || "Trade").replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 28) + "_Signed.pdf",
        date: tr.startDate || "2026-07-02",
        ownerSigned: true,
        ownerSignedBy: job.ownerName || "David & Sarah Kensington",
        ownerSignedDate: tr.startDate || "2026-07-02",
        dataUrl: ""
      };
    } else {
      if (!tr.contractPdf.date || !/^\d{4}-\d{2}-\d{2}$/.test(tr.contractPdf.date)) {
        tr.contractPdf.date = tr.startDate || "2026-07-02";
      }
      if (typeof tr.contractPdf.ownerSigned === "undefined") {
        tr.contractPdf.ownerSigned = true;
        tr.contractPdf.ownerSignedBy = job.ownerName || "David & Sarah Kensington";
        tr.contractPdf.ownerSignedDate = tr.contractPdf.date;
      }
    }
    if (typeof tr.customPct === "undefined") {
      if (tr.status === "Completed") tr.customPct = 100;
      else if (tr.contract > 0 && tr.billed > 0) tr.customPct = Math.min(99, Math.max(5, Math.round((tr.billed / tr.contract) * 100)));
      else tr.customPct = 0;
    }
  });
}

function getTradeCompletionPct(tr) {
  if (tr.status === "Completed") return 100;
  if (typeof tr.customPct === "number" && !isNaN(tr.customPct) && tr.customPct > 0) {
    return Math.min(100, Math.max(0, Math.round(tr.customPct)));
  }
  const c = Number(tr.contract) || 0;
  const b = Number(tr.billed) || 0;
  if (c > 0 && b > 0) return Math.min(99, Math.max(5, Math.round((b / c) * 100)));
  return 0;
}

function filterTradesTable(statusFilter, btn) {
  activeTradeFilter = "ALL";
  selectedP4TradeId = null;
  renderTradesList();
}

function toggleAddCustomTradeDrawer(forceOpen) {
  const el = document.getElementById("p4-add-custom-trade-drawer");
  if (!el) return;
  const shouldOpen = (typeof forceOpen === "boolean") ? forceOpen : (el.style.display === "none");
  el.style.display = shouldOpen ? "block" : "none";
}

function saveNewCustomTradeInline() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const nameEl = document.getElementById("p4-new-trade-name");
  const subEl = document.getElementById("p4-new-trade-sub");
  const startEl = document.getElementById("p4-new-trade-start");
  const endEl = document.getElementById("p4-new-trade-end");
  const amtEl = document.getElementById("p4-new-trade-amount");

  const name = (nameEl && nameEl.value.trim()) ? nameEl.value.trim() : "";
  if (!name) {
    showToast("Please enter a Trade Discipline & Name.");
    if (nameEl) nameEl.focus();
    return;
  }
  const sub = (subEl && subEl.value.trim()) ? subEl.value.trim() : "Assigned Trade Subcontractor";
  const startDate = (startEl && startEl.value) ? startEl.value : (job.whereWeAreDate || "2026-10-19");
  const endDate = (endEl && endEl.value) ? endEl.value : startDate;
  const contractAmt = Number(amtEl && amtEl.value) || 0;

  const nextNum = (job.trades || []).length + 1;
  const phaseStr = String(nextNum).padStart(2, "0");
  const newId = Date.now();
  const safePdf = "Stage_" + phaseStr + "_" + name.replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 28) + "_Contract.pdf";

  const newTrade = {
    id: newId,
    phase: phaseStr,
    name: name,
    sub: sub,
    contact: "Project Foreman",
    phone: "(604) 848-9688",
    startDate: startDate,
    endDate: endDate,
    contract: contractAmt,
    billed: 0,
    customPct: 0,
    gate: "Builder & Owner Quality Sign-Off",
    status: "Scheduled",
    contractPdf: {
      name: safePdf,
      date: startDate,
      ownerSigned: false,
      ownerSignedBy: "",
      ownerSignedDate: "",
      dataUrl: ""
    },
    docs: [safePdf],
    revisions: []
  };

  job.trades.push(newTrade);
  if (nameEl) nameEl.value = "";
  if (subEl) subEl.value = "";
  toggleAddCustomTradeDrawer(false);
  selectedP4TradeId = newId;
  saveState();
  renderAllPortalComponents();
  showToast("Added Stage " + phaseStr + ": " + name + " & opened its 3-section trade page");
}

function openAddTradeModal() {
  toggleAddCustomTradeDrawer(true);
}

function openP4TradeDetailPage(tradeId) {
  selectedP4TradeId = Number(tradeId);
  activeTradeModalId = Number(tradeId);
  renderTradesList();
}

function backToP4MasterTradesList() {
  selectedP4TradeId = null;
  renderTradesList();
}

function stepP4TradeDetail(delta) {
  const job = getActiveJob();
  const list = job.trades || [];
  if (!list.length) return;
  const idx = list.findIndex(t => Number(t.id) === Number(selectedP4TradeId));
  const nextIdx = (idx + delta + list.length) % list.length;
  selectedP4TradeId = list[nextIdx].id;
  activeTradeModalId = selectedP4TradeId;
  renderTradesList();
}

function renderTradesList() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);

  let totalContract = 0;
  let totalBilled = 0;
  (job.trades || []).forEach(t => {
    totalContract += Number(t.contract) || 0;
    totalBilled += Number(t.billed) || 0;
  });
  const revStats = getJobSignedRevisionsSum(job);

  const elC = document.getElementById("p4-kpi-total-contracts");
  const elCSub = document.getElementById("p4-kpi-contracts-sub");
  const elB = document.getElementById("p4-kpi-total-billed");
  const elH = document.getElementById("p4-kpi-total-holdback");
  const elR = document.getElementById("p4-kpi-revisions");
  const elRSub = document.getElementById("p4-kpi-revisions-sub");
  const cntBadge = document.getElementById("p4-trades-count-badge");

  const tradesCount = (job.trades || []).length;
  if (elC) elC.innerText = fmtMoney(totalContract);
  if (elCSub) elCSub.innerText = tradesCount + " Architect-to-Finish BC Scopes";
  if (elB) elB.innerText = fmtMoney(totalBilled);
  if (elH) elH.innerText = fmtMoney(Math.round(totalBilled * 0.10));
  if (elR) elR.innerText = (revStats.signedSum >= 0 ? "+" : "") + fmtMoney(revStats.signedSum);
  if (elRSub) {
    elRSub.innerText = revStats.pendingCount > 0
      ? (revStats.signedCount + " Accepted • " + revStats.pendingCount + " Pending")
      : (revStats.signedCount + " Accepted & Synced with Contract");
  }
  if (cntBadge) cntBadge.innerText = tradesCount + " Start-to-Finish Scopes";

  const listView = document.getElementById("p4-master-trades-list-view");
  const detailView = document.getElementById("p4-trade-detail-view");
  const listContainer = document.getElementById("p4-master-trades-list");
  if (!listView || !detailView || !listContainer) return;

  if (selectedP4TradeId !== null) {
    const activeTr = (job.trades || []).find(t => Number(t.id) === Number(selectedP4TradeId));
    if (activeTr) {
      listView.style.display = "none";
      detailView.style.display = "block";
      renderSelectedTrade3SectionPage(job, activeTr);
      return;
    }
    selectedP4TradeId = null;
  }

  listView.style.display = "block";
  detailView.style.display = "none";

  // Render clean Master List of All 22+ Trades:
  // Just Stage + Trade Name + "Date Active: From [Start Date] to [Finish Date]"
  listContainer.innerHTML = (job.trades || []).map(t => {
    const startStr = t.startDate || "TBD";
    const endStr = t.endDate || "TBD";
    return `
      <div class="kp-p4-trade-row" onclick="openP4TradeDetailPage(${t.id})">
        <div style="display:flex; align-items:center; gap:10px; min-width:0;">
          <span class="kp-badge-pill kp-badge-gold" style="flex-shrink:0;">STAGE ${escapeHtml(t.phase)}</span>
          <span style="font-size:0.86rem; font-weight:800; color:#ffffff; line-height:1.3;">
            ${escapeHtml(t.name)}
          </span>
        </div>

        <div style="display:flex; align-items:center; gap:8px; justify-content:flex-end; white-space:nowrap;">
          <span style="font-size:0.76rem; color:#cbd5e1; font-weight:700;">
            Date Active: <strong style="color:#ffffff;">${escapeHtml(startStr)}</strong> to <strong style="color:#ffffff;">${escapeHtml(endStr)}</strong>
          </span>
        </div>

        <div style="display:flex; justify-content:flex-end;">
          <button type="button" onclick="event.stopPropagation(); openP4TradeDetailPage(${t.id})" class="kp-secondary-btn kp-pill-sm">
            Open Trade (3 Sections) &rarr;
          </button>
        </div>
      </div>
    `;
  }).join("");
}

function getDisplayRevisionsForTrade(job, activeTrade) {
  const results = [];
  const seenKeys = new Set();

  // 1) First: Any revisions/change orders specifically on the active trade
  (activeTrade.revisions || []).forEach(r => {
    const key = String(activeTrade.id) + "::" + String(r.id);
    seenKeys.add(key);
    results.push({
      tradeId: activeTrade.id,
      tradePhase: activeTrade.phase,
      tradeName: activeTrade.name,
      tradeSub: activeTrade.sub,
      isCurrentTrade: true,
      rev: r
    });
  });

  // 2) Ensure the active trade's own IFC Scope Revision / Specification Addendum PDF is always listed
  const ifcId = "REV-" + activeTrade.phase;
  const ifcKey = String(activeTrade.id) + "::" + ifcId;
  if (!seenKeys.has(ifcKey)) {
    seenKeys.add(ifcKey);
    results.push({
      tradeId: activeTrade.id,
      tradePhase: activeTrade.phase,
      tradeName: activeTrade.name,
      tradeSub: activeTrade.sub,
      isCurrentTrade: true,
      rev: {
        id: ifcId,
        date: activeTrade.startDate || "2026-07-02",
        title: "Stage " + activeTrade.phase + " Issued for Construction (IFC) Scope & Schedule Revision",
        desc: "Approved Stage " + activeTrade.phase + " Field Scope, Engineering & Inspection Gate (" + (activeTrade.gate || "Builder & Engineer Sign-Off") + ")",
        amount: 0,
        pdfName: "Stage_" + activeTrade.phase + "_IFC_Scope_Revision.pdf",
        signed: true,
        signedBy: job.ownerName || "David & Sarah Kensington",
        signedDate: activeTrade.startDate || "2026-07-02",
        isBaselineScopeRev: true
      }
    });
  }

  // 3) Also include all Project Change Orders / Revisions across the build so the Owner always sees all revisions underneath
  (job.trades || []).forEach(tr => {
    (tr.revisions || []).forEach(r => {
      const key = String(tr.id) + "::" + String(r.id);
      if (!seenKeys.has(key)) {
        seenKeys.add(key);
        results.push({
          tradeId: tr.id,
          tradePhase: tr.phase,
          tradeName: tr.name,
          tradeSub: tr.sub,
          isCurrentTrade: (Number(tr.id) === Number(activeTrade.id)),
          rev: r
        });
      }
    });
  });

  return results;
}

function renderSelectedTrade3SectionPage(job, t) {
  const detailView = document.getElementById("p4-trade-detail-view");
  if (!detailView) return;

  const pct = getTradeCompletionPct(t);
  const holdbackAmt = Math.round((Number(t.billed) || 0) * 0.10);
  const revs = t.revisions || [];
  const acceptedRevSum = revs.filter(r => r.signed).reduce((acc, r) => acc + (Number(r.amount) || 0), 0);
  const revisedTradeTotal = (Number(t.contract) || 0) + acceptedRevSum;
  const allDisplayRevs = getDisplayRevisionsForTrade(job, t);
  const jobRevStats = getJobSignedRevisionsSum(job);

  const cPdf = t.contractPdf || {
    name: "Stage_" + t.phase + "_Subcontract_Signed.pdf",
    date: t.startDate || "2026-07-02",
    ownerSigned: true,
    ownerSignedBy: job.ownerName || "David & Sarah Kensington",
    ownerSignedDate: t.startDate || "2026-07-02"
  };

  const tradeOptionsHtml = (job.trades || []).map(item => `
    <option value="${item.id}" ${Number(item.id) === Number(t.id) ? "selected" : ""}>
      Stage ${escapeHtml(item.phase)} — ${escapeHtml(item.name)}
    </option>
  `).join("");

  detailView.innerHTML = `
    <!-- Top Navigation Bar Inside Trade Page -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; background:#0b0f17; border:1px solid #d4af37; border-radius:12px; padding:11px 15px; margin-bottom:14px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <button type="button" onclick="backToP4MasterTradesList()" class="kp-gold-btn kp-pill-sm">
          &larr; Back to All ${(job.trades || []).length} Trades List
        </button>
        <span class="kp-badge-pill kp-badge-white">STAGE ${escapeHtml(t.phase)} OF ${(job.trades || []).length}</span>
        <span style="font-size:0.94rem; font-weight:900; color:#ffffff;">${escapeHtml(t.name)}</span>
      </div>

      <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap;">
        <button type="button" onclick="stepP4TradeDetail(-1)" class="kp-secondary-btn kp-pill-sm">&larr; Prev Trade</button>
        <select
          onchange="openP4TradeDetailPage(this.value)"
          style="background:#05070b !important; border:1px solid rgba(255,255,255,0.24) !important; color:#ffffff !important; border-radius:9999px !important; padding:4px 28px 4px 12px !important; font-size:0.74rem !important; font-weight:800 !important; height:32px !important; width:auto !important; max-width:290px !important; margin:0 !important; cursor:pointer !important;"
        >
          ${tradeOptionsHtml}
        </select>
        <button type="button" onclick="stepP4TradeDetail(1)" class="kp-secondary-btn kp-pill-sm">Next Trade &rarr;</button>
      </div>
    </div>

    <!-- ===================================================================
         SECTION 1 OF 3: TRADE CONTRACT, DATE & OWNER SIGNATURE
         (Sign, Open/Print on Screen, Download PDF, Upload PDF)
         =================================================================== -->
    <div class="kp-p4-detail-section">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.12);">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">SECTION 1 OF 3 &bull; TRADE CONTRACT &amp; OWNER SIGN-OFF</span>
          <span class="kp-badge-pill kp-badge-white">
            ${cPdf.ownerSigned ? ("✓ Signed by " + escapeHtml(cPdf.ownerSignedBy || job.ownerName) + " (" + escapeHtml(cPdf.ownerSignedDate || cPdf.date) + ")") : "Awaiting Owner Signature"}
          </span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="signTradeContractByOwner(${t.id})" class="kp-gold-btn kp-pill-sm">
            ${cPdf.ownerSigned ? "✓ Contract Signed (Click to Update Sign-Off)" : "Sign Trade Contract (Owner & Builder)"}
          </button>
        </div>
      </div>

      <!-- Contract Details & Editable Contract Date Grid -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(195px, 1fr)); gap:10px; margin-bottom:12px;">
        <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 13px;">
          <div style="font-size:0.66rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Subcontractor Company</div>
          <input
            type="text"
            id="p4-sec1-sub"
            value="${escapeHtml(t.sub || "")}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="margin-top:4px; height:32px; padding:4px 10px; font-weight:800;"
          />
          <div style="font-size:0.7rem; color:#cbd5e1; margin-top:4px;">Contact: ${escapeHtml(t.contact || "Project Foreman")} &bull; ${escapeHtml(t.phone || "(604) 848-9688")}</div>
        </div>

        <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 13px;">
          <div style="font-size:0.66rem; font-weight:800; color:#d4af37; text-transform:uppercase;">Contract Signed Date</div>
          <input
            type="date"
            id="p4-sec1-contract-date"
            value="${escapeHtml(cPdf.date || t.startDate || "2026-07-02")}"
            onchange="updateTradeContractDate(${t.id}, this.value)"
            class="kp-form-input"
            style="margin-top:4px; height:32px; padding:4px 10px; font-weight:800; color-scheme:dark;"
          />
          <div style="font-size:0.7rem; color:#cbd5e1; margin-top:4px;">Builder: Wayne Stevenson (#52603)</div>
        </div>

        <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 13px;">
          <div style="font-size:0.66rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Base Subcontract Amount ($ CAD)</div>
          <input
            type="number"
            id="p4-sec1-contract-amt"
            value="${Number(t.contract) || 0}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="margin-top:4px; height:32px; padding:4px 10px; font-weight:900; color:#ffffff;"
          />
          <div style="font-size:0.7rem; color:#d4af37; font-weight:700; margin-top:4px;">
            With Revisions: ${fmtMoney(revisedTradeTotal)}
          </div>
        </div>

        <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 13px;">
          <div style="font-size:0.66rem; font-weight:800; color:#94a3b8; text-transform:uppercase;">Invoiced To Date &amp; 10% Holdback</div>
          <input
            type="number"
            id="p4-sec1-billed-amt"
            value="${Number(t.billed) || 0}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="margin-top:4px; height:32px; padding:4px 10px; font-weight:900; color:#d4af37;"
          />
          <div style="font-size:0.7rem; color:#cbd5e1; margin-top:4px;">
            10% Lien Holdback: <strong style="color:#ffffff;">${fmtMoney(holdbackAmt)}</strong>
          </div>
        </div>
      </div>

      <!-- Contract PDF File Bar (Open & Print on Screen, Download PDF, Upload PDF) -->
      <div style="background:#05070b; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; align-items:center; gap:9px; min-width:0; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">SIGNED TRADE CONTRACT PDF</span>
          <span style="font-size:0.82rem; font-weight:800; color:#ffffff;">${escapeHtml(cPdf.name)}</span>
          <span style="font-size:0.73rem; color:#cbd5e1;">
            &bull; Contract Date: <strong style="color:#f3e5ab;">${escapeHtml(cPdf.date || t.startDate)}</strong>
            &bull; ${cPdf.ownerSigned ? ("Co-Signed by " + escapeHtml(cPdf.ownerSignedBy || job.ownerName)) : "Ready for Owner Signature"}
          </span>
        </div>

        <div style="display:flex; gap:7px; align-items:center; flex-wrap:wrap;">
          <button type="button" onclick="openTradeContractPdfOnScreen(${t.id})" class="kp-gold-btn kp-pill-sm">
            Open &amp; Print PDF on Screen
          </button>
          <button type="button" onclick="downloadTradeContractPdf(${t.id})" class="kp-secondary-btn kp-pill-sm">
            Download PDF
          </button>
          <label class="kp-secondary-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            Upload Contract PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleP4TradeContractUpload(${t.id}, event)" />
          </label>
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SECTION 2 OF 3: TRADE TIMELINE & WHERE THEY ARE SITTING
         (Date Active From -> To, % Complete, Status & Inspection Gate)
         =================================================================== -->
    <div class="kp-p4-detail-section">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-bottom:10px; margin-bottom:12px; border-bottom:1px solid rgba(255,255,255,0.12);">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">SECTION 2 OF 3 &bull; TIMELINE &amp; WHERE THEY ARE SITTING</span>
          <span class="kp-badge-pill kp-badge-white">
            Date Active: ${escapeHtml(t.startDate || "TBD")} to ${escapeHtml(t.endDate || "TBD")}
          </span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="kp-badge-pill kp-badge-gold">${pct}% COMPLETE &bull; ${escapeHtml(t.status || "Scheduled").toUpperCase()}</span>
          <button type="button" onclick="saveP4TradeSectionUpdates(${t.id}, true)" class="kp-gold-btn kp-pill-sm">
            Save Timeline Updates
          </button>
        </div>
      </div>

      <!-- Visual Progress Bar ("Where They Are Sitting") -->
      <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:11px 14px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-size:0.78rem;">
          <span style="color:#ffffff; font-weight:800;">
            Where Stage ${escapeHtml(t.phase)} Is Sitting Right Now: <strong style="color:#d4af37;">${escapeHtml(t.status)} (${pct}% Done)</strong>
          </span>
          <span style="color:#cbd5e1; font-size:0.73rem;">
            QA Milestone Gate: <strong style="color:#ffffff;">${escapeHtml(t.gate || "Builder & Engineer Sign-Off")}</strong>
          </span>
        </div>
        <div style="width:100%; height:10px; background:#05070b; border:1px solid rgba(255,255,255,0.18); border-radius:9999px; overflow:hidden;">
          <div style="width:${pct}%; height:100%; background:linear-gradient(90deg, #d4af37 0%, #f3e5ab 100%); border-radius:9999px;"></div>
        </div>
      </div>

      <!-- Editable Timeline Dates, Completion % & Status Controls -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(185px, 1fr)); gap:10px;">
        <div>
          <label class="kp-form-label" style="color:#ffffff;">Date Active From (Start Date)</label>
          <input
            type="date"
            id="p4-sec2-start"
            value="${escapeHtml(t.startDate || "")}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="color-scheme:dark; font-weight:800;"
          />
        </div>
        <div>
          <label class="kp-form-label" style="color:#ffffff;">Date Active To (Finish Date)</label>
          <input
            type="date"
            id="p4-sec2-end"
            value="${escapeHtml(t.endDate || "")}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="color-scheme:dark; font-weight:800;"
          />
        </div>
        <div>
          <label class="kp-form-label" style="color:#ffffff;">Where Sitting (% Complete)</label>
          <input
            type="number"
            id="p4-sec2-pct"
            min="0"
            max="100"
            value="${pct}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="font-weight:900; color:#d4af37;"
          />
        </div>
        <div>
          <label class="kp-form-label" style="color:#ffffff;">Stage Status</label>
          <select
            id="p4-sec2-status"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
            style="font-weight:800;"
          >
            <option value="Completed" ${t.status === "Completed" ? "selected" : ""}>Completed (100%)</option>
            <option value="Active On-Site" ${t.status === "Active On-Site" ? "selected" : ""}>Active On-Site</option>
            <option value="Scheduled" ${t.status === "Scheduled" ? "selected" : ""}>Scheduled</option>
          </select>
        </div>
        <div>
          <label class="kp-form-label" style="color:#ffffff;">QA / Inspection Gate</label>
          <input
            type="text"
            id="p4-sec2-gate"
            value="${escapeHtml(t.gate || "")}"
            onchange="saveP4TradeSectionUpdates(${t.id})"
            class="kp-form-input"
          />
        </div>
      </div>
    </div>

    <!-- ===================================================================
         SECTION 3 OF 3: REVISIONS & CHANGE ORDERS LIST
         (Clean List of All Revisions Underneath — Click Any Revision to Open PDF)
         =================================================================== -->
    <div class="kp-p4-detail-section" style="margin-bottom:0 !important;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-bottom:10px; margin-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.12);">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">SECTION 3 OF 3 &bull; REVISIONS &amp; CHANGE ORDERS</span>
          <span class="kp-badge-pill kp-badge-white">
            ${allDisplayRevs.length} Revisions Listed &bull; Accepted Total: +${fmtMoney(jobRevStats.signedSum)}
          </span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span style="font-size:0.73rem; color:#cbd5e1; font-weight:600;">
            Click any revision below to bring up its PDF on screen
          </span>
          <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            + Upload Revision PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleP4ChangeOrderPdfUpload(${t.id}, event)" />
          </label>
        </div>
      </div>

      <!-- Clean Clickable List of All Revisions Underneath (Click Any Row -> Opens PDF on Screen) -->
      <div style="display:flex; flex-direction:column; gap:8px;">
        ${allDisplayRevs.map(item => {
          const r = item.rev;
          const pdfFile = r.pdfName || (r.id + "_Revision_Signed.pdf");
          const amtNum = Number(r.amount) || 0;
          const amtText = amtNum > 0 ? ("+" + fmtMoney(amtNum)) : "Included in Base Contract";
          return `
            <div
              class="kp-p4-rev-row"
              onclick="openChangeOrderPdfOnScreen('${item.tradeId}', '${escapeHtml(r.id)}')"
              style="border-color:${item.isCurrentTrade ? "rgba(212,175,55,0.48)" : "rgba(255,255,255,0.18)"} !important;"
              title="Click to open ${escapeHtml(pdfFile)} on screen"
            >
              <div style="min-width:0; flex:1;">
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                  <span class="kp-badge-pill ${item.isCurrentTrade ? "kp-badge-gold" : "kp-badge-white"}">
                    ${escapeHtml(r.id)} &bull; STAGE ${escapeHtml(item.tradePhase)}
                  </span>
                  <span class="kp-badge-pill ${r.signed ? "kp-badge-gold" : "kp-badge-white"}">
                    ${r.signed ? "✓ ACCEPTED & SIGNED" : "PENDING OWNER SIGN-OFF"}
                  </span>
                  <span style="font-size:0.86rem; font-weight:900; color:#ffffff;">
                    ${escapeHtml(r.title)}
                  </span>
                  <span style="font-size:0.84rem; font-weight:900; color:#d4af37;">
                    ${escapeHtml(amtText)}
                  </span>
                </div>
                <div style="font-size:0.73rem; color:#cbd5e1; margin-top:4px;">
                  <strong style="color:#ffffff;">${escapeHtml(item.tradeName)}</strong> (${escapeHtml(item.tradeSub)})
                  &bull; Date: <strong style="color:#f3e5ab;">${escapeHtml(r.date || "2026-10-15")}</strong>
                  &bull; PDF: <strong style="color:#ffffff;">${escapeHtml(pdfFile)}</strong>
                </div>
              </div>

              <div style="display:flex; gap:7px; align-items:center; flex-wrap:wrap;" onclick="event.stopPropagation();">
                ${!r.signed ? `
                  <button type="button" onclick="acceptAndSignP4ChangeOrder('${item.tradeId}', '${escapeHtml(r.id)}')" class="kp-gold-btn kp-pill-sm">
                    Accept &amp; Sign (Owner)
                  </button>
                ` : ""}
                <button type="button" onclick="openChangeOrderPdfOnScreen('${item.tradeId}', '${escapeHtml(r.id)}')" class="kp-gold-btn kp-pill-sm">
                  Open Revision PDF
                </button>
                <button type="button" onclick="downloadRevisionPdf('${item.tradeId}', '${escapeHtml(r.id)}')" class="kp-secondary-btn kp-pill-sm">
                  Download PDF
                </button>
              </div>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  `;
}

function saveP4TradeSectionUpdates(tradeId, showFeedback) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;

  const subEl = document.getElementById("p4-sec1-sub");
  const cAmtEl = document.getElementById("p4-sec1-contract-amt");
  const bAmtEl = document.getElementById("p4-sec1-billed-amt");
  const startEl = document.getElementById("p4-sec2-start");
  const endEl = document.getElementById("p4-sec2-end");
  const pctEl = document.getElementById("p4-sec2-pct");
  const statusEl = document.getElementById("p4-sec2-status");
  const gateEl = document.getElementById("p4-sec2-gate");

  if (subEl) t.sub = subEl.value.trim() || t.sub;
  if (cAmtEl) t.contract = Number(cAmtEl.value) || 0;
  if (bAmtEl) t.billed = Number(bAmtEl.value) || 0;
  if (startEl && startEl.value) t.startDate = startEl.value;
  if (endEl && endEl.value) t.endDate = endEl.value;
  if (pctEl) {
    t.customPct = Math.min(100, Math.max(0, Number(pctEl.value) || 0));
  }
  if (statusEl && statusEl.value) {
    t.status = statusEl.value;
    if (t.status === "Completed") t.customPct = 100;
  }
  if (gateEl) t.gate = gateEl.value.trim() || t.gate;

  saveState();
  renderAllPortalComponents();
  if (showFeedback) {
    showToast("Saved Stage " + t.phase + " Contract & Timeline (Synced with Live Calendar & Project Capital)");
  }
}

function updateTradeContractDate(tradeId, newDateISO) {
  if (!newDateISO) return;
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  t.contractPdf = t.contractPdf || {};
  t.contractPdf.date = newDateISO;
  saveState();
  renderTradesList();
  showToast("Updated Stage " + t.phase + " Contract Date to " + newDateISO);
}

function signTradeContractByOwner(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const todayISO = job.whereWeAreDate || "2026-10-17";
  t.contractPdf = t.contractPdf || {};
  t.contractPdf.ownerSigned = true;
  t.contractPdf.ownerSignedBy = job.ownerName || "David & Sarah Kensington";
  t.contractPdf.ownerSignedDate = todayISO;
  if (!t.contractPdf.date) t.contractPdf.date = todayISO;
  saveState();
  renderTradesList();
  showToast("Stage " + t.phase + " Trade Contract Co-Signed by " + t.contractPdf.ownerSignedBy + " & Wayne Stevenson (#52603)");
}

function openTradeContractPdfOnScreen(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const cPdf = t.contractPdf || { name: "Stage_" + t.phase + "_Subcontract_Signed.pdf", date: t.startDate || "2026-07-02" };
  const revs = (t.revisions || []).filter(r => r.signed);
  const revSum = revs.reduce((a, r) => a + (Number(r.amount) || 0), 0);
  const bodyLines = [
    "STAGE " + t.phase + " SUBCONTRACT AGREEMENT: " + t.name,
    "SUBCONTRACTOR: " + t.sub + " (" + (t.contact || "Project Foreman") + " • " + (t.phone || "(604) 848-9688") + ")",
    "CONTRACT DATE: " + (cPdf.date || t.startDate) + " | ACTIVE SCHEDULE: " + (t.startDate || "TBD") + " to " + (t.endDate || "TBD"),
    "BASE SUBCONTRACT AMOUNT: " + fmtMoney(t.contract),
    "ACCEPTED CHANGE ORDERS: +" + fmtMoney(revSum) + " | REVISED SUBCONTRACT TOTAL: " + fmtMoney((Number(t.contract) || 0) + revSum),
    "INVOICED TO DATE: " + fmtMoney(t.billed) + " | 10% BUILDERS LIEN HOLDBACK: " + fmtMoney(Math.round((Number(t.billed) || 0) * 0.10)),
    "INSPECTION & QUALITY GATE: " + (t.gate || "Builder & Engineer Sign-Off"),
    "SIGNATURE STATUS: Executed & Co-Signed by Wayne Stevenson (BC Licensed Builder #52603) and Property Owner(s) " + (cPdf.ownerSignedBy || job.ownerName) + "."
  ].join("\n\n");

  openCustomVaultPdfOnScreen(
    "Stage " + t.phase + " Trade Subcontract — " + t.name,
    cPdf.name,
    t.sub + " • Contract Date: " + (cPdf.date || t.startDate) + " • " + fmtMoney(t.contract),
    bodyLines,
    cPdf.dataUrl || ""
  );
}

function handleP4TradeContractUpload(tradeId, ev) {
  const file = ev && ev.target && ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    const cDateEl = document.getElementById("p4-sec1-contract-date");
    const chosenDate = (cDateEl && cDateEl.value) ? cDateEl.value : (t.startDate || "2026-10-17");
    t.contractPdf = {
      name: file.name,
      date: chosenDate,
      ownerSigned: true,
      ownerSignedBy: job.ownerName || "David & Sarah Kensington",
      ownerSignedDate: chosenDate,
      dataUrl: e.target.result || ""
    };
    saveState();
    renderTradesList();
    showToast("Uploaded Signed Trade Contract PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function handleP4ChangeOrderPdfUpload(tradeId, ev) {
  const file = ev && ev.target && ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;

  const coDate = job.whereWeAreDate || "2026-10-17";
  const cleanFileTitle = file.name.replace(/\.[^/.]+$/, "").replace(/[_-]+/g, " ");

  const reader = new FileReader();
  reader.onload = function(e) {
    t.revisions = t.revisions || [];
    const revId = "CO-" + t.phase + "-" + (t.revisions.length + 1);
    t.revisions.push({
      id: revId,
      date: coDate,
      title: cleanFileTitle,
      desc: "Uploaded Revision / Change Order PDF (" + file.name + ")",
      amount: 0,
      days: 0,
      pdfName: file.name,
      signed: true,
      signedBy: job.ownerName || "David & Sarah Kensington",
      signedDate: coDate,
      dataUrl: e.target.result || ""
    });
    saveState();
    renderAllPortalComponents();
    showToast("Uploaded Revision PDF: " + file.name + " (Click it in the list to open on screen)");
  };
  reader.readAsDataURL(file);
}

function acceptAndSignP4ChangeOrder(tradeId, revId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => String(x.id) === String(tradeId));
  if (!t) return;
  const rev = (t.revisions || []).find(r => String(r.id) === String(revId));
  if (!rev) return;
  const todayISO = job.whereWeAreDate || "2026-10-17";
  rev.signed = true;
  rev.signedBy = job.ownerName || "David & Sarah Kensington";
  rev.signedDate = todayISO;
  saveState();
  renderAllPortalComponents();
  showToast("Accepted & Signed Revision " + rev.id + " (+" + fmtMoney(rev.amount) + ")");
}

function resolveRevisionRecord(job, tradeId, revId) {
  const t = (job.trades || []).find(x => String(x.id) === String(tradeId)) || (job.trades || [])[0];
  if (!t) return null;
  let rev = (t.revisions || []).find(r => String(r.id) === String(revId));
  if (!rev && String(revId) === ("REV-" + t.phase)) {
    rev = {
      id: "REV-" + t.phase,
      date: t.startDate || "2026-07-02",
      title: "Stage " + t.phase + " Issued for Construction (IFC) Scope & Schedule Revision",
      desc: "Approved Stage " + t.phase + " Field Scope, Engineering & Inspection Gate (" + (t.gate || "Builder & Engineer Sign-Off") + ")",
      amount: 0,
      pdfName: "Stage_" + t.phase + "_IFC_Scope_Revision.pdf",
      signed: true,
      signedBy: job.ownerName || "David & Sarah Kensington",
      signedDate: t.startDate || "2026-07-02"
    };
  }
  return rev ? { trade: t, rev: rev } : null;
}

function openChangeOrderPdfOnScreen(tradeId, revId) {
  const job = getActiveJob();
  const resolved = resolveRevisionRecord(job, tradeId, revId);
  if (!resolved) return;
  const t = resolved.trade;
  const rev = resolved.rev;
  const amtNum = Number(rev.amount) || 0;
  const amtText = amtNum > 0 ? ("+" + fmtMoney(amtNum)) : "Included in Base Subcontract (" + fmtMoney(t.contract) + ")";

  const body = [
    "REVISION / CHANGE ORDER REFERENCE: " + rev.id + " (Stage " + t.phase + " — " + t.name + ")",
    "SUBCONTRACTOR: " + t.sub + " (" + (t.contact || "Project Foreman") + " • " + (t.phone || "(604) 848-9688") + ")",
    "REVISION DATE: " + (rev.date || "2026-10-15") + " | ACTIVE STAGE WINDOW: " + (t.startDate || "TBD") + " to " + (t.endDate || "TBD"),
    "REVISION / CHANGE ORDER TITLE: " + rev.title,
    "DETAILED SCOPE & ENGINEERING SPECIFICATION: " + (rev.desc || rev.title),
    "COST IMPACT: " + amtText,
    "ACCEPTANCE & SIGN-OFF STATUS: " + (rev.signed ? ("ACCEPTED & SIGNED by " + (rev.signedBy || job.ownerName) + " and Wayne Stevenson (BC Licensed Builder #52603) on " + (rev.signedDate || rev.date)) : "Pending Property Owner Acceptance")
  ].join("\n\n");

  openCustomVaultPdfOnScreen(
    rev.id + " — " + rev.title,
    rev.pdfName || (rev.id + "_Revision_Signed.pdf"),
    "Stage " + t.phase + " Revision • " + amtText + " • " + (rev.date || "2026-10-15"),
    body,
    rev.dataUrl || ""
  );
}

function downloadRevisionPdf(tradeId, revId) {
  const job = getActiveJob();
  const resolved = resolveRevisionRecord(job, tradeId, revId);
  if (!resolved) return;
  const t = resolved.trade;
  const rev = resolved.rev;
  const pdfFile = rev.pdfName || (rev.id + "_Revision_Signed.pdf");
  const amtNum = Number(rev.amount) || 0;
  const amtText = amtNum > 0 ? ("+" + fmtMoney(amtNum)) : "Included in Base Subcontract";
  const content = [
    "REVISION / CHANGE ORDER: " + rev.id + " - " + rev.title,
    "STAGE " + t.phase + ": " + t.name + " (" + t.sub + ")",
    "DATE: " + (rev.date || "2026-10-15") + " | COST IMPACT: " + amtText,
    "DETAILS: " + (rev.desc || rev.title),
    "STATUS: " + (rev.signed ? ("Signed & Accepted by " + (rev.signedBy || job.ownerName)) : "Pending Owner Signature")
  ].join("\n");
  triggerDummyDownload(pdfFile, content, rev.dataUrl || "");
  showToast("Downloaded Revision PDF: " + pdfFile);
}

function openTradeModal(tradeId) {
  // Always close legacy #modal-trade if open and route directly to Page 4's 3-Section Trade View
  const oldModal = document.getElementById("modal-trade");
  if (oldModal) oldModal.classList.remove("open");
  const btn4 = document.querySelector('.kp-nav-tab[data-tab="4"]');
  if (typeof switchPortalPage === "function") {
    switchPortalPage(4, btn4);
  }
  openP4TradeDetailPage(tradeId);
}

function exportTradesSummary() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const rows = [
    "Stage,Trade Discipline & Name,Subcontractor,Contact,Phone,Date Active From,Date Active To,Completion %,Status,Base Contract ($),Accepted Change Orders ($),Revised Total ($),Invoiced To Date ($),10% Lien Holdback ($),Signed Contract PDF,Contract Date"
  ];
  (job.trades || []).forEach(t => {
    const pct = getTradeCompletionPct(t);
    const hold = Math.round((Number(t.billed) || 0) * 0.10);
    const revSum = (t.revisions || []).filter(r => r.signed).reduce((a, r) => a + (Number(r.amount) || 0), 0);
    const revTotal = (Number(t.contract) || 0) + revSum;
    const pdfName = (t.contractPdf && t.contractPdf.name) ? t.contractPdf.name : ("Stage_" + t.phase + "_Signed.pdf");
    const pdfDate = (t.contractPdf && t.contractPdf.date) ? t.contractPdf.date : (t.startDate || "");
    rows.push(
      `"Stage ${t.phase}","${String(t.name || "").replace(/"/g, '""')}","${String(t.sub || "").replace(/"/g, '""')}","${String(t.contact || "").replace(/"/g, '""')}","${String(t.phone || "").replace(/"/g, '""')}","${t.startDate || ""}","${t.endDate || ""}",${pct}%,${t.status},${Number(t.contract) || 0},${revSum},${revTotal},${Number(t.billed) || 0},${hold},"${pdfName}","${pdfDate}"`
    );
  });
  const blob = new Blob([rows.join("\r\n")], { type: "text/csv;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = job.jobId + "_Updated_Master_Trades_Schedule.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  showToast("Exported Updated Master Trade Schedule CSV (" + (job.trades || []).length + " Scopes)");
}

function exportTradesSchedulePdf() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const lines = (job.trades || []).map(t => {
    const revSum = (t.revisions || []).filter(r => r.signed).reduce((a, r) => a + (Number(r.amount) || 0), 0);
    return `Stage ${t.phase}: ${t.name} | Active: ${t.startDate} to ${t.endDate} | Contract: ${fmtMoney(t.contract)} (+CO: ${fmtMoney(revSum)}) | Billed: ${fmtMoney(t.billed)}`;
  });
  const pdfFile = job.jobId + "_Updated_30_Stage_Master_Trades_Schedule.pdf";
  triggerDummyDownload(pdfFile, lines.join("\n"));
  showToast("Exported Updated Master Trade Schedule PDF");
}



let lastSuggestedTakeoffRows = [];

const DEFAULT_P5_SECTION_ORDER = [
  { key: "civil",      label: "1. Civil" },
  { key: "excavation", label: "2. Excavation" },
  { key: "concrete",   label: "3. Concrete" },
  { key: "framing",    label: "4. Framing" },
  { key: "roofing",    label: "5. Roofing" },
  { key: "siding",     label: "6. Siding" },
  { key: "finishing",  label: "7. Finishing" }
];

function ensureMaterialSections7Boxes(job) {
  if (!job) return;
  if (typeof job.costPlus10Enabled !== "boolean") {
    job.costPlus10Enabled = true;
  }
  const s = (job.contractPrice && job.contractPrice > 2500000) ? (job.contractPrice / 1850000) : 1.0;
  const r = (n) => Math.round((n * s) / 100) * 100;

  if (!job.materialSectionDefs || !Array.isArray(job.materialSectionDefs) || job.materialSectionDefs.length < 7) {
    job.materialSectionDefs = DEFAULT_P5_SECTION_ORDER.map(x => ({ key: x.key, label: x.label }));
  }

  if (!job.materialSectionsVault || !job.materialSectionsVault.excavation || !job.materialSectionsVault.roofing || !job.materialSectionsVault.siding) {
    job.materialSectionsVault = {
      civil: [
        {
          id: "CIV-02",
          listNum: 2,
          dateISO: "2026-08-28",
          title: "Second Material List — Storm, Sanitary & Watermain Underground Piping",
          supplier: "EMCO Waterworks Squamish",
          pdfName: job.jobId + "_Civil_List_02_Storm_Watermain.pdf",
          invoiceNum: "INV-EMCO-88412",
          baseCost: r(14200),
          paid: true,
          paidDate: "2026-09-02",
          items: [
            "6\" SDR35 PVC Storm Sewer Main Pipe — 180 LF",
            "4\" Perforated PVC Foundation Weeping Tile + Filter Sock — 210 LF",
            "Precast Concrete Storm Catch Basin + Heavy Cast Iron Grate — 2 Sets",
            "2\" Type K Soft Copper Municipal Water Service Line + Curb Stop — 85 LF",
            "4\" Cast Iron Backwater Valve & Cleanout Riser Assembly — 4 Sets"
          ]
        },
        {
          id: "CIV-01",
          listNum: 1,
          dateISO: "2026-08-18",
          title: "First Material List — BC Hydro Underground Ducts, Pull Box & Erosion Control",
          supplier: "Andrew Sheret Civil & Infrastructure",
          pdfName: job.jobId + "_Civil_List_01_Hydro_Ducts.pdf",
          invoiceNum: "INV-ASC-87104",
          baseCost: r(9800),
          paid: true,
          paidDate: "2026-08-24",
          items: [
            "3\" DB2 PVC Underground Electrical & Telecom Conduit (10' Lengths) — 44 Pcs",
            "BC Hydro Approved Precast Concrete Underground Splice Box — 1 Unit",
            "Municipal Tree Protection Hoarding + Silt Fence Rolls — 240 LF",
            "Warning Tape & Tracer Wire for Buried Civil Services — 4 Rolls"
          ]
        }
      ],
      excavation: [
        {
          id: "EXC-02",
          listNum: 2,
          dateISO: "2026-08-14",
          title: "Second Material List — 3/4\" Clear Crush Drain Rock & Structural Subbase Aggregate",
          supplier: "Mainland Sand & Gravel / Squamish Quarry",
          pdfName: job.jobId + "_Excavation_List_02_Crush_Aggregate.pdf",
          invoiceNum: "INV-MSG-44219",
          baseCost: r(12400),
          paid: true,
          paidDate: "2026-08-19",
          items: [
            "3/4\" (19mm) Clear Washed Crushed Foundation Drain Rock — 68 Tons",
            "75mm Minus Crushed Structural Road & Footing Subbase Aggregate — 110 Tons",
            "Non-Woven Geotextile Separation Filter Fabric (15'x300' Roll) — 4 Rolls",
            "Clean Structural Backfill Sand & Compacted Granular Fill — 54 Tons"
          ]
        },
        {
          id: "EXC-01",
          listNum: 1,
          dateISO: "2026-08-06",
          title: "First Material List — Bedrock Dowels, Rock Anchors & Structural Epoxy",
          supplier: "Williams Form Hardware & Hilti Canada",
          pdfName: job.jobId + "_Excavation_List_01_Bedrock_Anchors.pdf",
          invoiceNum: "INV-WFH-41908",
          baseCost: r(8900),
          paid: true,
          paidDate: "2026-08-11",
          items: [
            "25M Williams Grade 400W Deformed Bedrock Dowels (10' Lengths) — 26 Pcs",
            "Hilti HIT-RE 500 V3 Structural Rock Anchor Epoxy Cartridges — 18 Tubes",
            "Heavy-Duty Bearing Plates, Hex Nuts & Galvanized Rock Washers — 26 Sets",
            "Rock Micro-Splitting Wedges, Feathers & Drill Bits — 12 Sets"
          ]
        }
      ],
      concrete: [
        {
          id: "CON-02",
          listNum: 2,
          dateISO: "2026-09-25",
          title: "Second Material List — 35 MPa Ready-Mix Concrete, XPS Insulation & Vapor Barrier",
          supplier: "Cardinal Concrete Squamish / Brock White",
          pdfName: job.jobId + "_Concrete_List_02_35MPa_ReadyMix.pdf",
          invoiceNum: "INV-CARD-60215",
          baseCost: r(24800),
          paid: true,
          paidDate: "2026-09-30",
          items: [
            "35 MPa Sulfate-Resistant Ready-Mix Structural Concrete — 64 m³",
            "Owens Corning Foamular C-200 2\" XPS Underslab Rigid Insulation (4x8) — 56 Sheets",
            "15-Mil Stego Wrap Class A Underslab Vapor Barrier + Seam Tape — 4 Rolls",
            "6x6-10/10 Welded Wire Reinforcing Mesh Sheets (8'x20') — 34 Sheets",
            "1/2\" x 10\" Hot-Dip Galvanized Sill Anchor Bolts + Plate Washers — 48 Pcs"
          ]
        },
        {
          id: "CON-01",
          listNum: 1,
          dateISO: "2026-09-10",
          title: "First Material List — Formwork 2x6 / 2x4 Lumber, HDO Form Ply & 15M/20M Rebar",
          supplier: "Dick's Lumber & Building Supplies / Harris Rebar",
          pdfName: job.jobId + "_Concrete_List_01_Formwork_Rebar.pdf",
          invoiceNum: "INV-DL-58910",
          baseCost: r(19400),
          paid: true,
          paidDate: "2026-09-18",
          items: [
            "2x6 x 16' #2&Btr SPF Foundation Form Walers & Bracing — 26 Pcs",
            "2x4 x 16' #2&Btr SPF Form Stakes, Kickers & Spreaders — 120 Pcs",
            "3/4\" HDO Overlaid Concrete Form Plywood (4x8 Sheets) — 64 Sheets",
            "15M Grade 400W Deformed Reinforcing Steel Rebar (20' Lengths) — 185 Pcs",
            "20M Grade 400W Continuous Footing & Corner Dowel Bar — 92 Pcs",
            "Delta-MS Foundation Dimple Dampproofing Membrane — 16 Rolls"
          ]
        }
      ],
      framing: [
        {
          id: "FRM-03",
          listNum: 3,
          dateISO: "2026-10-16",
          title: "Third Material List — Roof Trusses, 2x6 Fascia, 5/8\" Fir Roof Sheathing & Ties",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Framing_List_03_Roof_Trusses_Sheathing.pdf",
          invoiceNum: "INV-DL-71409",
          baseCost: r(22600),
          paid: false,
          paidDate: "",
          items: [
            "2x6 x 16' KD Douglas Fir #1&Btr Fascia & Barge Rafters — 26 Pcs",
            "Engineered Wood Roof Trusses (6:12 Pitch, 42 psf Snow Load) — 34 Trusses",
            "5/8\" 5-Ply Douglas Fir CDX Roof Deck Sheathing (4x8) + H-Clips — 78 Sheets",
            "Simpson Strong-Tie H2.5A Galvanized Seismic Hurricane Truss Ties — 68 Pcs",
            "3-1/4\" Hot-Dip Galvanized Framing Nails (2,500/Box) — 14 Boxes"
          ]
        },
        {
          id: "FRM-02",
          listNum: 2,
          dateISO: "2026-10-14",
          title: "Second Material List — Main & 2nd Storey 2x6 / 2x4 Studs, PT Sill Plates & Sheathing",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Framing_List_02_2x6_Wall_Studs.pdf",
          invoiceNum: "INV-DL-70882",
          baseCost: r(28400),
          paid: true,
          paidDate: "2026-10-15",
          items: [
            "2x6 x 16' Pressure-Treated Hem-Fir Mudsill Plates + Sill Gasket — 26 Pcs",
            "2x6 x 104-5/8\" (9' Wall) KD SPF #2&Btr Exterior Wall Studs — 380 Pcs",
            "2x6 x 16' KD SPF Bottom & Double Top Exterior Wall Plates — 142 Pcs",
            "2x4 x 104-5/8\" (9' Wall) KD SPF #2&Btr Interior Partition Studs — 460 Pcs",
            "1-3/4\" x 11-7/8\" 2.0E Microllam LVL Window & Door Headers — 26 Pcs",
            "1/2\" 4-Ply Douglas Fir CDX Exterior Shear Wall Sheathing (4x8) — 96 Sheets"
          ]
        },
        {
          id: "FRM-01",
          listNum: 1,
          dateISO: "2026-10-10",
          title: "First Material List — Engineered TJI Floor Joists, Glulam Beams & 3/4\" Subfloor",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Framing_List_01_TJI_Subfloor.pdf",
          invoiceNum: "INV-DL-69914",
          baseCost: r(24900),
          paid: true,
          paidDate: "2026-10-12",
          items: [
            "11-7/8\" Weyerhaeuser TJI 230 Engineered I-Joists (@ 16\" O.C.) — 48 Pcs",
            "1-3/4\" x 11-7/8\" TimberStrand LSL Rim Board (16' Lengths) — 26 Pcs",
            "5-1/8\" x 15\" Architectural Grade Douglas Fir Glulam Drop Beams — 6 Pcs",
            "3/4\" T&G Weyerhaeuser EdgeGold Water-Resistant OSB Subfloor (4x8) — 112 Sheets",
            "28oz LePage PL400 Heavy-Duty Subfloor Adhesive Cartridges — 70 Tubes",
            "Simpson Strong-Tie HDU8-SDS2.5 Seismic Hold-Downs & ITS Joist Hangers — 54 Pcs"
          ]
        }
      ],
      roofing: [
        {
          id: "ROF-02",
          listNum: 2,
          dateISO: "2026-11-10",
          title: "Second Material List — 24-Gauge Standing Seam Metal Roof Panels & Ridge Cap",
          supplier: "Westform Metals / Pacific Rim Roofing Supply",
          pdfName: job.jobId + "_Roofing_List_02_Standing_Seam_Metal.pdf",
          invoiceNum: "INV-WFM-81204",
          baseCost: r(18600),
          paid: false,
          paidDate: "",
          items: [
            "24-Gauge Matte Black Standing Seam Architectural Metal Roof Panels — 3,450 SF",
            "24-Gauge Pre-Painted Vented Ridge Cap, Gable Rake & Valley Flashing — 320 LF",
            "Concealed Stainless Steel Floating Standing Seam Clips & Screws — 1,200 Pcs",
            "Color-Matched Heavy-Duty Alpine Snow Guards — 48 Units"
          ]
        },
        {
          id: "ROF-01",
          listNum: 1,
          dateISO: "2026-11-05",
          title: "First Material List — High-Temp Ice & Water Shield, Synthetic Underlay & Drip Edge",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Roofing_List_01_Underlayment_Flashing.pdf",
          invoiceNum: "INV-DL-78112",
          baseCost: r(6400),
          paid: false,
          paidDate: "",
          items: [
            "Grace Ice & Water Shield High-Temp Peel-and-Stick Roof Membrane — 14 Rolls",
            "Titanium UDL30 Synthetic Breathable Roof Underlayment — 8 Rolls",
            "26-Gauge Matte Black Eave Drip Edge & Plumbing Stack Flashing Boots — 280 LF"
          ]
        }
      ],
      siding: [
        {
          id: "SID-02",
          listNum: 2,
          dateISO: "2026-11-26",
          title: "Second Material List — James Hardie Architectural Panel, Lap Siding & Clear Cedar Soffit",
          supplier: "Dick's Lumber Building Envelope Division",
          pdfName: job.jobId + "_Siding_List_02_Hardie_Cedar_Soffit.pdf",
          invoiceNum: "INV-DL-84019",
          baseCost: r(21500),
          paid: false,
          paidDate: "",
          items: [
            "James Hardie Aspyre Architectural Fiber-Cement Panels (4x10) — 74 Sheets",
            "James Hardie Cedarmill 7-1/4\" Lap Siding Planks (12' Lengths) — 190 Pcs",
            "1x6 Clear Kiln-Dried Western Red Cedar T&G Soffit Boards — 1,150 LF",
            " Tamlyn Extruded Aluminum J-Mold, Reveal & Horizontal Z-Flashing — 420 LF"
          ]
        },
        {
          id: "SID-01",
          listNum: 1,
          dateISO: "2026-11-18",
          title: "First Material List — Tyvek DrainWrap, 1x4 Pressure-Treated Rainscreen Strapping & Bug Screen",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Siding_List_01_Rainscreen_Envelope.pdf",
          invoiceNum: "INV-DL-82105",
          baseCost: r(7200),
          paid: false,
          paidDate: "",
          items: [
            "1x4 x 8' Pressure-Treated Hem-Fir Vertical Rainscreen Furring Strips — 420 Pcs",
            "DuPont Tyvek DrainWrap Commercial Weather Barrier + Seam Tape — 9 Rolls",
            "3M All-Weather Window & Door Sill Pan Flashing Membrane (6\" & 9\") — 12 Rolls",
            "Cor-A-Vent Insect Screen Roll for Top & Bottom Rainscreen Cavities — 10 Rolls"
          ]
        }
      ],
      finishing: [
        {
          id: "FIN-02",
          listNum: 2,
          dateISO: "2026-12-14",
          title: "Second Material List — Solid Core Interior Doors, White Oak Casing, Baseboard & Hardware",
          supplier: "Dick's Lumber Finishing Division / Windsor Plywood",
          pdfName: job.jobId + "_Finishing_List_02_Doors_Trim_Hardware.pdf",
          invoiceNum: "INV-DL-91204",
          baseCost: r(15200),
          paid: false,
          paidDate: "",
          items: [
            "1-3/4\" Solid Core Shaker Interior Doors (8'0\" Height, Pre-Hung) — 26 Doors",
            "1x6 & 1x4 Paint-Grade / White Oak Baseboard & Door/Window Casing — 1,450 LF",
            "Emtek Matte Black Modern Rectangular Lever Sets & Ball-Bearing Hinges — 26 Sets",
            "18-Gauge Brad Nails, Finishing Putty & Acoustical Sealant Caulk — 16 Boxes"
          ]
        },
        {
          id: "FIN-01",
          listNum: 1,
          dateISO: "2026-12-02",
          title: "First Material List — 5/8\" Firecode Drywall, Rockwool Insulation & Corner Bead",
          supplier: "Dick's Lumber & Building Supplies",
          pdfName: job.jobId + "_Finishing_List_01_Drywall_Insulation.pdf",
          invoiceNum: "INV-DL-88912",
          baseCost: r(11800),
          paid: false,
          paidDate: "",
          items: [
            "5/8\" CGC Sheetrock Firecode X Gypsum Drywall Board (4x12 Sheets) — 240 Sheets",
            "Rockwool Comfortbatt R24 Exterior Wall + Safe'n'Sound Acoustic Batts — 68 Bags",
            "6-Mil CGSB Polyethylene Vapor Barrier + Tuck Tape — 10 Rolls",
            "Paper-Faced Metal Drywall Corner Bead & Joint Compound Pails — 24 Pails"
          ]
        }
      ]
    };
  }
}

function getSortedSectionLists(job, secKey) {
  ensureMaterialSections7Boxes(job);
  const arr = (job.materialSectionsVault && job.materialSectionsVault[secKey]) ? job.materialSectionsVault[secKey] : [];
  // Newest ones go to the top
  return arr.slice().sort((a, b) => {
    const da = String(a.dateISO || "");
    const db = String(b.dateISO || "");
    if (db !== da) return db.localeCompare(da);
    return (Number(b.listNum) || 0) - (Number(a.listNum) || 0);
  });
}

function toggleP5CostPlusMode() {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  job.costPlus10Enabled = !job.costPlus10Enabled;
  saveState();
  renderMaterialsList();
  showToast(job.costPlus10Enabled
    ? "10% Plus Cost ENABLED on Material Invoices"
    : "Switched to Base Supplier Cost Only (0% Markup)");
}

function calculateSmartTakeoff() {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const planName = (job.takeoffParams && job.takeoffParams.planPdfName)
    ? job.takeoffParams.planPdfName
    : (job.jobId + "_Framing_Takeoff_Blueprint_Set.pdf");
  const badgeEl = document.getElementById("p5-plan-pdf-badge");
  const metaEl = document.getElementById("p5-plan-pdf-meta");
  if (badgeEl) badgeEl.innerText = planName;
  if (metaEl) metaEl.innerText = "• Permit #" + (job.permitNum || "BP2026-0419");
}

function openActivePlanTakeoffPdfOnScreen() {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const planName = (job.takeoffParams && job.takeoffParams.planPdfName)
    ? job.takeoffParams.planPdfName
    : (job.jobId + "_Framing_Takeoff_Blueprint_Set.pdf");
  const dataUrl = (job.takeoffParams && job.takeoffParams.planPdfDataUrl) ? job.takeoffParams.planPdfDataUrl : "";
  if (dataUrl) {
    openCustomVaultPdfOnScreen(
      "Active Plans PDF",
      planName,
      job.address + " • Permit #" + (job.permitNum || "BP2026-0419"),
      "Uploaded Architectural & Structural Plan Set.",
      dataUrl
    );
  } else {
    openPortalPdfViewer("arch");
  }
}

function renderMaterialsList() {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  calculateSmartTakeoff();

  const cpBtn = document.getElementById("p5-btn-cost-plus-toggle");
  if (cpBtn) {
    cpBtn.className = job.costPlus10Enabled ? "kp-gold-btn kp-pill-sm" : "kp-secondary-btn kp-pill-sm";
    cpBtn.innerHTML = job.costPlus10Enabled ? "10% Plus Cost: ON &#10003;" : "10% Plus Cost: OFF (Base Cost)";
  }

  let allBase = 0;
  let allMarkup = 0;
  let allTotal = 0;
  let paidSum = 0;
  let unpaidSum = 0;
  let paidCount = 0;
  let unpaidCount = 0;

  (job.materialSectionDefs || []).forEach(sec => {
    const lists = getSortedSectionLists(job, sec.key);
    lists.forEach(item => {
      const base = Number(item.baseCost) || 0;
      const markup = job.costPlus10Enabled ? Math.round(base * 0.10) : 0;
      const total = base + markup;
      allBase += base;
      allMarkup += markup;
      allTotal += total;
      if (item.paid) {
        paidSum += total;
        paidCount++;
      } else {
        unpaidSum += total;
        unpaidCount++;
      }
    });
  });

  const bEl = document.getElementById("mat-total-budget");
  const mEl = document.getElementById("p5-kpi-markup-val");
  const mSub = document.getElementById("p5-kpi-markup-sub");
  const aEl = document.getElementById("mat-total-actual");
  const vEl = document.getElementById("mat-total-var");
  const pSub = document.getElementById("p5-kpi-paid-sub");

  if (bEl) bEl.innerText = fmtMoney(allBase);
  if (mEl) mEl.innerText = job.costPlus10Enabled ? ("+" + fmtMoney(allMarkup)) : "$0";
  if (mSub) mSub.innerText = job.costPlus10Enabled ? "10% Plus Cost Applied on Invoices" : "0% Markup (Base Supplier Cost)";
  if (aEl) aEl.innerText = fmtMoney(allTotal);
  if (vEl) vEl.innerText = fmtMoney(paidSum) + " Paid";
  if (pSub) {
    pSub.innerText = paidCount + " Paid (" + fmtMoney(paidSum) + ") • " + unpaidCount + " Not Paid (" + fmtMoney(unpaidSum) + ")";
  }

  const wrap = document.getElementById("kp-material-accordions");
  if (!wrap) return;

  wrap.innerHTML = (job.materialSectionDefs || []).map(sec => {
    const lists = getSortedSectionLists(job, sec.key);

    const rowsHtml = lists.map((pkg, idx) => {
      const numLabel = pkg.listNum ? ("#" + pkg.listNum) : ("#" + (lists.length - idx));
      return `
        <div
          style="background:#05070b; border:1px solid ${pkg.paid ? "rgba(212,175,55,0.42)" : "rgba(255,255,255,0.16)"}; border-radius:10px; padding:9px 13px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; transition:all 0.15s ease;"
        >
          <!-- LEFT: Clickable Material Takeoff List (Opens PDF of JUST the List of Materials) -->
          <div
            onclick="openMaterialTakeoffListPdf('${escapeHtml(sec.key)}', '${escapeHtml(pkg.id)}')"
            style="display:flex; align-items:center; gap:10px; min-width:0; flex:1; cursor:pointer;"
            title="Click to open the PDF list of materials needed (${escapeHtml(pkg.pdfName)})"
          >
            <span class="kp-badge-pill kp-badge-gold" style="min-width:44px; text-align:center;">
              ${escapeHtml(numLabel)}
            </span>
            <span style="font-size:0.86rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
              ${escapeHtml(pkg.title)}
            </span>
          </div>

          <!-- RIGHT: Date + Paid/Not Paid Button Beside It (Opens Invoice PDF) -->
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <span
              onclick="openMaterialTakeoffListPdf('${escapeHtml(sec.key)}', '${escapeHtml(pkg.id)}')"
              style="font-size:0.76rem; color:#cbd5e1; font-weight:700; cursor:pointer;"
              title="Click to open the PDF list of materials"
            >
              Date: <strong style="color:#ffffff;">${escapeHtml(pkg.dateISO)}</strong>
            </span>

            <button
              type="button"
              onclick="openMaterialInvoicePdf('${escapeHtml(sec.key)}', '${escapeHtml(pkg.id)}')"
              class="${pkg.paid ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm"
              style="min-width:128px; justify-content:center;"
              title="Click to open the Invoice PDF, see if it is Paid or Not Paid, and when it was paid"
            >
              ${pkg.paid ? ("✓ PAID (" + escapeHtml(pkg.paidDate || pkg.dateISO) + ")") : "NOT PAID"}
            </button>
          </div>
        </div>
      `;
    }).join("");

    return `
      <div style="background:#080c14; border:1px solid rgba(212,175,55,0.28); border-radius:12px; padding:12px 15px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px; padding-bottom:6px; border-bottom:1px solid rgba(255,255,255,0.1);">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.94rem; font-weight:900; color:#ffffff; letter-spacing:0.03em;">
              ${escapeHtml(sec.label)}
            </span>
            <span class="kp-badge-pill kp-badge-white">
              ${lists.length} Material List${lists.length === 1 ? "" : "s"} (Newest at Top)
            </span>
          </div>

          <div style="display:flex; align-items:center; gap:6px;">
            <button type="button" onclick="promptAddMaterialListToSection('${escapeHtml(sec.key)}')" class="kp-secondary-btn kp-pill-sm">
              + Add Material List
            </button>
          </div>
        </div>

        <!-- Scrollable List Inside Each Section Box (Newest at Top) -->
        <div style="display:flex; flex-direction:column; gap:6px; max-height:195px; overflow-y:auto; padding-right:2px;">
          ${rowsHtml}
        </div>
      </div>
    `;
  }).join("");
}

// 1. CLICK ON MATERIAL LIST -> Opens PDF of JUST the List of Materials Needed (for Dick's Lumber / Supplier)
function openMaterialTakeoffListPdf(secKey, pkgId) {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const list = job.materialSectionsVault[secKey] || [];
  const pkg = list.find(x => String(x.id) === String(pkgId));
  if (!pkg) return;

  const secDef = (job.materialSectionDefs || []).find(s => s.key === secKey) || { label: secKey.toUpperCase() };
  const numberedItems = (pkg.items || []).map((line, i) => `${i + 1}. ${line}`);

  const lines = [
    "SECTION: " + secDef.label.toUpperCase() + " — MATERIAL TAKEOFF LIST",
    "MATERIAL LIST: #" + (pkg.listNum || 1) + " — " + pkg.title,
    "DATE: " + pkg.dateISO + " | SUPPLIER: " + pkg.supplier,
    "------------------------------------------------------------------------",
    "MATERIALS NEEDED (LIST ONLY):",
    ...numberedItems
  ];

  openCustomVaultPdfOnScreen(
    "Material List #" + (pkg.listNum || 1) + " — " + pkg.title,
    pkg.pdfName,
    secDef.label + " • Date: " + pkg.dateISO + " • Supplier: " + pkg.supplier,
    lines.join("\n\n"),
    pkg.dataUrl || ""
  );
}

// 2. CLICK ON PAID / NOT PAID BESIDE IT -> Opens the Invoice PDF (Shows Invoice, Paid/Not Paid Status, When It Was Paid & Cost + 10%)
function openMaterialInvoicePdf(secKey, pkgId) {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const list = job.materialSectionsVault[secKey] || [];
  const pkg = list.find(x => String(x.id) === String(pkgId));
  if (!pkg) return;

  const secDef = (job.materialSectionDefs || []).find(s => s.key === secKey) || { label: secKey.toUpperCase() };
  const base = Number(pkg.baseCost) || 0;
  const markup = job.costPlus10Enabled ? Math.round(base * 0.10) : 0;
  const total = base + markup;
  const invFile = pkg.pdfName.replace(/\.pdf$/i, "") + "_INVOICE.pdf";

  const modal = document.getElementById("modal-pdf-viewer");
  const titleEl = document.getElementById("pdf-modal-title");
  const bodyEl = document.getElementById("pdf-modal-body");
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (!modal || !bodyEl) return;

  if (titleEl) {
    titleEl.innerText = "Invoice — " + pkg.title + " (" + (pkg.paid ? ("PAID ON " + (pkg.paidDate || pkg.dateISO)) : "NOT PAID") + ")";
  }

  const pdfLines = [
    "MATERIAL SUPPLIER INVOICE & PAYMENT RECORD",
    "SECTION: " + secDef.label.toUpperCase(),
    "INVOICE NUMBER: " + (pkg.invoiceNum || ("INV-" + pkg.id)) + " | MATERIAL LIST DATE: " + pkg.dateISO,
    "SUPPLIER: " + pkg.supplier,
    "PAYMENT STATUS: " + (pkg.paid ? ("PAID IN FULL ✓ — PAID ON: " + (pkg.paidDate || pkg.dateISO)) : "NOT PAID / OUTSTANDING"),
    "------------------------------------------------------------------------",
    "INVOICED MATERIAL ITEMS:",
    ...(pkg.items || []).map((line, i) => `  ${i + 1}. ${line}`),
    "------------------------------------------------------------------------",
    "SUPPLIER BASE MATERIAL COST: " + fmtMoney(base),
    "BUILDER 10% PLUS COST FEE: " + (job.costPlus10Enabled ? ("+" + fmtMoney(markup) + " (10% Plus Cost)") : "$0"),
    "TOTAL INVOICE AMOUNT: " + fmtMoney(total)
  ];

  if (dlBtn) {
    dlBtn.innerText = "Download Invoice PDF";
    dlBtn.onclick = () => triggerDummyDownload(invFile, pdfLines.join("\n"));
  }

  bodyEl.innerHTML = `
    <!-- Top Invoice Status & 1-Click Paid / Not Paid Toggle Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; background:#0b0f17; border:1px solid rgba(212,175,55,0.45); border-radius:9999px; padding:8px 16px; margin:0 auto 16px auto; max-width:850px;">
      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <span class="kp-badge-pill ${pkg.paid ? "kp-badge-gold" : "kp-badge-white"}">
          ${pkg.paid ? ("✓ INVOICE PAID — PAID ON " + escapeHtml(pkg.paidDate || pkg.dateISO)) : "INVOICE STATUS: NOT PAID"}
        </span>
        <span style="font-size:0.76rem; color:#ffffff; font-weight:800;">
          Total: ${fmtMoney(total)} ${job.costPlus10Enabled ? "(Includes 10% Plus Cost)" : "(Base Cost)"}
        </span>
      </div>
      <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
        <button
          type="button"
          onclick="toggleMaterialInvoicePaidModal('${escapeHtml(secKey)}', '${escapeHtml(pkg.id)}')"
          class="${pkg.paid ? "kp-secondary-btn" : "kp-gold-btn"} kp-pill-sm"
        >
          ${pkg.paid ? "Mark as Not Paid" : "✓ Mark Invoice Paid Today"}
        </button>
        <button type="button" onclick="window.print()" class="kp-secondary-btn kp-pill-sm">Print Invoice</button>
      </div>
    </div>

    <!-- Clean Printable White Invoice Sheet -->
    <div class="kp-pdf-page-sheet">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:16px; margin-bottom:18px;">
        <div>
          <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.1em; color:#b45309; text-transform:uppercase;">
            ${escapeHtml(secDef.label)} &bull; MATERIAL INVOICE &amp; PAYMENT STATUS
          </div>
          <h2 style="font-size:1.35rem; font-weight:900; color:#0f172a; margin:4px 0 2px 0; font-family:'Outfit','Plus Jakarta Sans',sans-serif;">
            ${escapeHtml(pkg.supplier)}
          </h2>
          <div style="font-size:0.84rem; font-weight:700; color:#1e293b;">
            ${escapeHtml(pkg.title)}
          </div>
        </div>
        <div style="text-align:right;">
          <div style="background:${pkg.paid ? "#0f172a" : "#7f1d1d"}; color:${pkg.paid ? "#d4af37" : "#ffffff"}; font-weight:900; font-size:0.76rem; padding:6px 12px; border-radius:4px;">
            ${pkg.paid ? ("✓ PAID IN FULL • " + escapeHtml(pkg.paidDate || pkg.dateISO)) : "STATUS: NOT PAID"}
          </div>
          <div style="font-size:0.74rem; color:#475569; margin-top:5px;">
            Invoice #: <strong>${escapeHtml(pkg.invoiceNum || ("INV-" + pkg.id))}</strong> &bull; Order Date: <strong>${escapeHtml(pkg.dateISO)}</strong>
          </div>
        </div>
      </div>

      <!-- Payment Verification Box -->
      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:12px 16px; margin-bottom:18px; display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; font-size:0.8rem;">
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Payment Status</div>
          <div style="font-size:0.92rem; font-weight:900; color:#0f172a; margin-top:2px;">
            ${pkg.paid ? "PAID OFF ✓" : "NOT PAID (OUTSTANDING)"}
          </div>
        </div>
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Date Invoice Was Paid</div>
          <div style="font-size:0.92rem; font-weight:900; color:#0f172a; margin-top:2px;">
            ${pkg.paid ? escapeHtml(pkg.paidDate || pkg.dateISO) : "Pending Payment"}
          </div>
        </div>
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Project / Permit</div>
          <div style="font-size:0.84rem; font-weight:800; color:#0f172a; margin-top:2px;">
            ${escapeHtml(job.address)} (#${escapeHtml(job.permitNum || "BP2026-0419")})
          </div>
        </div>
      </div>

      <!-- Material Line Items on Invoice -->
      <div style="font-size:0.74rem; font-weight:900; text-transform:uppercase; color:#0f172a; letter-spacing:0.06em; border-bottom:1px solid #cbd5e1; padding-bottom:4px; margin-bottom:10px;">
        Invoiced Materials List (${(pkg.items || []).length} Items)
      </div>
      <div style="margin-bottom:20px;">
        ${(pkg.items || []).map((line, i) => `
          <div style="padding:7px 10px; border-bottom:1px solid #e2e8f0; font-size:0.83rem; font-weight:700; color:#0f172a;">
            ${i + 1}. ${escapeHtml(line)}
          </div>
        `).join("")}
      </div>

      <!-- Cost + 10% Financial Summary Table -->
      <table style="width:100%; border-collapse:collapse; font-size:0.84rem; margin-top:10px;">
        <tbody>
          <tr style="border-bottom:1px solid #cbd5e1;">
            <td style="padding:8px 10px; font-weight:700; color:#334155;">Supplier Material Cost (Base Invoice)</td>
            <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">${fmtMoney(base)}</td>
          </tr>
          <tr style="border-bottom:1px solid #cbd5e1;">
            <td style="padding:8px 10px; font-weight:700; color:#334155;">Builder 10% Plus Cost Fee (${job.costPlus10Enabled ? "10% Applied" : "0%"})</td>
            <td style="padding:8px 10px; text-align:right; font-weight:800; color:#0f172a;">+${fmtMoney(markup)}</td>
          </tr>
          <tr style="background:#fefce8; border-top:2px solid #0f172a; border-bottom:2px solid #0f172a;">
            <td style="padding:10px; font-weight:900; color:#0f172a;">TOTAL MATERIAL INVOICE (${pkg.paid ? ("PAID ON " + escapeHtml(pkg.paidDate || pkg.dateISO)) : "NOT PAID"})</td>
            <td style="padding:10px; text-align:right; font-weight:900; font-size:1.05rem; color:#0f172a;">${fmtMoney(total)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `;

  modal.classList.add("open");
  modal.style.display = "flex";
}

function toggleMaterialInvoicePaidModal(secKey, pkgId) {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const list = job.materialSectionsVault[secKey] || [];
  const pkg = list.find(x => String(x.id) === String(pkgId));
  if (!pkg) return;
  pkg.paid = !pkg.paid;
  pkg.paidDate = pkg.paid ? (job.whereWeAreDate || "2026-10-17") : "";
  saveState();
  renderMaterialsList();
  openMaterialInvoicePdf(secKey, pkgId);
  showToast(pkg.paid
    ? ("Invoice Marked PAID ✓ (Paid Date: " + pkg.paidDate + ")")
    : "Invoice Marked NOT PAID");
}

function promptAddMaterialListToSection(secKey) {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const secDef = (job.materialSectionDefs || []).find(s => s.key === secKey) || { label: secKey };
  const listArr = job.materialSectionsVault[secKey] || (job.materialSectionsVault[secKey] = []);
  const nextNum = listArr.length + 1;

  const titleInput = prompt(`Enter title for ${secDef.label} Material List #${nextNum}:`, `Material List #${nextNum} — Additional ${secDef.label.replace(/^[0-9.]+\s*/, "")} Materials`);
  if (!titleInput) return;
  const itemsInput = prompt("Enter materials needed (comma-separated, e.g. 2x6x16 SPF — 26 Pcs, 1/2\" Fir Sheathing — 40 Sheets):", "2x6 x 16' KD SPF Lumber — 26 Pcs, 1/2\" Douglas Fir Sheathing (4x8) — 32 Sheets");
  if (itemsInput === null) return;
  const costInput = prompt("Enter Supplier Base Cost ($ CAD):", "8500");
  const todayISO = job.whereWeAreDate || "2026-10-17";

  listArr.unshift({
    id: secKey.slice(0, 3).toUpperCase() + "-0" + nextNum,
    listNum: nextNum,
    dateISO: todayISO,
    title: titleInput.trim(),
    supplier: "Dick's Lumber & Building Supplies",
    pdfName: `${job.jobId}_${secKey}_Material_List_0${nextNum}.pdf`,
    invoiceNum: `INV-DL-${Math.floor(70000 + Math.random() * 20000)}`,
    baseCost: Number(String(costInput || "8500").replace(/[^0-9.]/g, "")) || 8500,
    paid: false,
    paidDate: "",
    items: String(itemsInput || "").split(",").map(s => s.trim()).filter(Boolean)
  });

  saveState();
  renderMaterialsList();
  showToast(`Added Material List #${nextNum} to ${secDef.label}`);
}

function promptAddCustomMaterialSection() {
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const name = prompt("Enter new Material Section name (e.g., Landscaping, Windows, Decking):");
  if (!name || !name.trim()) return;
  const cleanLabel = (job.materialSectionDefs.length + 1) + ". " + name.trim();
  const key = name.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_") + "_" + Date.now().toString().slice(-3);
  job.materialSectionDefs.push({ key, label: cleanLabel });
  job.materialSectionsVault[key] = [
    {
      id: key.slice(0, 3).toUpperCase() + "-01",
      listNum: 1,
      dateISO: job.whereWeAreDate || "2026-10-17",
      title: "First Material List — " + name.trim() + " Package",
      supplier: "Dick's Lumber & Building Supplies",
      pdfName: `${job.jobId}_${key}_Material_List_01.pdf`,
      invoiceNum: "INV-DL-94110",
      baseCost: 9500,
      paid: false,
      paidDate: "",
      items: [
        name.trim() + " Primary Material Takeoff Item #1 — 26 Pcs",
        name.trim() + " Fasteners, Hardware & Accessories — 1 Lot"
      ]
    }
  ];
  saveState();
  renderMaterialsList();
  showToast("Added new section box: " + cleanLabel);
}

function handleTakeoffPlanPdfUpload(ev) {
  const file = ev && ev.target && ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  ensureMaterialSections7Boxes(job);
  const reader = new FileReader();
  reader.onload = function(e) {
    job.takeoffParams = job.takeoffParams || {};
    job.takeoffParams.planPdfName = file.name;
    job.takeoffParams.planPdfDataUrl = e.target.result || "";
    saveState();
    renderMaterialsList();
    showToast("Updated Active Plans PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function exportMaterialsCSV() {
  openActivePlanTakeoffPdfOnScreen();
}



// ============================================================================
// TAB 6: HIGHLAND MULTIPLEX MASTER FINANCIALS & ALL-PDFS LEDGER
// - Top: 4-Card Keystone Master Money Breakdown
// - Middle: 5 Live-Synced Sections (1. Trades, 2. Materials, 3. City, 4. Architect, 5. Engineer)
// - Bottom: Highland Master Tally (Paid, Unpaid & How Much We Are At)
// ============================================================================

function ensureMasterFinancialLedgerVault(job) {
  if (!job) return;
  ensureArchitectToFinish22Trades(job);
  ensureMaterialSections7Boxes(job);
  ensureJobDatedVaultDocs(job);

  if (!job.p6StatusOverrides) {
    job.p6StatusOverrides = {};
  }
  if (!job.p6CustomEntries) {
    job.p6CustomEntries = {
      trades: [],
      materials: [],
      city: [],
      architect: [],
      engineer: []
    };
  }
}

function collectHighland5SectionsData(job) {
  ensureMasterFinancialLedgerVault(job);
  const s = (job.contractPrice && job.contractPrice > 2500000) ? (job.contractPrice / 1850000) : 1.0;
  const r = (n) => Math.round((n * s) / 100) * 100;

  // 1. TRADES (Live from job.trades: Completed/Active Draws + Change Order PDFs)
  const tradeRows = [];
  (job.trades || []).forEach(tr => {
    const billed = Number(tr.billed) || 0;
    const contract = Number(tr.contract) || 0;
    if (billed > 0) {
      const rowKey = "TRD-DRAW-" + tr.id;
      const ov = job.p6StatusOverrides[rowKey] || {};
      const isPaid = (typeof ov.paid === "boolean") ? ov.paid : true;
      const amt = (typeof ov.amount === "number") ? ov.amount : billed;
      tradeRows.push({
        rowKey,
        secKey: "trades",
        badge: "STAGE " + tr.phase,
        title: tr.name + " — " + tr.sub + (billed < contract ? " (Certified Progress Draw)" : " (100% Stage Contract)"),
        dateISO: tr.endDate || tr.startDate || "2026-10-14",
        pdfName: tr.contractPdfName || (job.jobId + "_Stage" + tr.phase + "_Signed_Trade_Contract.pdf"),
        amount: amt,
        paid: isPaid,
        paidDate: ov.paidDate || tr.endDate || "2026-10-14",
        openPdfFn: `openP6MasterPdfItem('trades', '${rowKey}')`,
        desc: `Executed Subcontract & Certified Progress Draw for Stage ${tr.phase}: ${tr.name} (${tr.sub}). Active: ${tr.startDate} to ${tr.endDate}.`
      });
    }
    // If stage is currently In Progress (e.g. Stage 09 Framing), also show the remaining active balance as an Unpaid upcoming draw
    if (tr.status === "In Progress" && contract > billed) {
      const remAmt = contract - billed;
      const rowKey = "TRD-REM-" + tr.id;
      const ov = job.p6StatusOverrides[rowKey] || {};
      const isPaid = (typeof ov.paid === "boolean") ? ov.paid : false;
      const amt = (typeof ov.amount === "number") ? ov.amount : remAmt;
      tradeRows.push({
        rowKey,
        secKey: "trades",
        badge: "STAGE " + tr.phase + " BAL",
        title: tr.name + " — Remaining Stage Completion Draw (" + tr.sub + ")",
        dateISO: tr.endDate || "2026-11-06",
        pdfName: job.jobId + "_Stage" + tr.phase + "_Completion_Draw_Invoice.pdf",
        amount: amt,
        paid: isPaid,
        paidDate: ov.paidDate || "",
        openPdfFn: `openP6MasterPdfItem('trades', '${rowKey}')`,
        desc: `Remaining Stage ${tr.phase} completion draw balance for ${tr.sub} (${tr.name}).`
      });
    }
    // Include all Change Orders / Revisions PDFs
    (tr.revisions || []).forEach(rev => {
      const rowKey = "TRD-REV-" + rev.id;
      const ov = job.p6StatusOverrides[rowKey] || {};
      const isPaid = (typeof ov.paid === "boolean") ? ov.paid : Boolean(rev.signed);
      const amt = (typeof ov.amount === "number") ? ov.amount : (Number(rev.amount) || 0);
      tradeRows.push({
        rowKey,
        secKey: "trades",
        badge: rev.id,
        title: "Change Order: " + rev.title + " (Stage " + tr.phase + " — " + tr.sub + ")",
        dateISO: rev.date || "2026-10-12",
        pdfName: rev.pdfName || (job.jobId + "_" + rev.id + "_Change_Order.pdf"),
        amount: amt,
        paid: isPaid,
        paidDate: ov.paidDate || rev.signedDate || rev.date || "2026-10-12",
        openPdfFn: `openTradeRevisionPdfModal('${tr.id}', '${rev.id}')`,
        desc: rev.desc || ("Revision " + rev.id + " under Stage " + tr.phase)
      });
    });
  });
  (job.p6CustomEntries.trades || []).forEach(c => tradeRows.unshift(c));

  // 2. MATERIALS (Live from job.materialSectionsVault across all 7 Material Sections on Page 5)
  const materialRows = [];
  (job.materialSectionDefs || []).forEach(sec => {
    const lists = getSortedSectionLists(job, sec.key);
    lists.forEach(pkg => {
      const base = Number(pkg.baseCost) || 0;
      const markup = job.costPlus10Enabled ? Math.round(base * 0.10) : 0;
      const total = base + markup;
      materialRows.push({
        rowKey: "MAT-" + sec.key + "-" + pkg.id,
        secKey: "materials",
        matSecKey: sec.key,
        matPkgId: pkg.id,
        badge: sec.label.replace(/^[0-9.]+\s*/, "").toUpperCase(),
        title: pkg.title + " (" + pkg.supplier + ")",
        dateISO: pkg.dateISO || "2026-10-14",
        pdfName: pkg.pdfName,
        amount: total,
        paid: Boolean(pkg.paid),
        paidDate: pkg.paidDate || pkg.dateISO || "",
        openPdfFn: `openMaterialTakeoffListPdf('${sec.key}', '${pkg.id}')`,
        openInvFn: `openMaterialInvoicePdf('${sec.key}', '${pkg.id}')`,
        desc: `Material Takeoff & Invoice (${pkg.supplier}) — Base: ${fmtMoney(base)} + 10% Cost-Plus (${fmtMoney(markup)}) = ${fmtMoney(total)}.`
      });
    });
  });
  (job.p6CustomEntries.materials || []).forEach(c => materialRows.unshift(c));

  // 3. CITY / DISTRICT OF SQUAMISH (Live from job.datedVaultDocs.city + Municipal Permit & Inspection Fees)
  const defaultCityAmounts = [r(28500), r(1250), r(1250), r(1500), r(1250), r(1250)];
  const cityDocs = getSortedCategoryDocs(job, "city");
  const cityRows = cityDocs.map((doc, idx) => {
    const rowKey = "CTY-DOC-" + doc.id;
    const ov = job.p6StatusOverrides[rowKey] || {};
    const defaultAmt = defaultCityAmounts[idx % defaultCityAmounts.length];
    const isPaid = (typeof ov.paid === "boolean") ? ov.paid : true;
    const amt = (typeof ov.amount === "number") ? ov.amount : defaultAmt;
    return {
      rowKey,
      secKey: "city",
      badge: doc.code || "CITY PDF",
      title: doc.title,
      dateISO: doc.dateISO || "2026-10-14",
      pdfName: doc.pdfName,
      amount: amt,
      paid: isPaid,
      paidDate: ov.paidDate || doc.dateISO || "2026-10-14",
      openPdfFn: `openP6MasterPdfItem('city', '${rowKey}')`,
      desc: doc.bodyText || doc.sub || "Official District of Squamish inspection & permit PDF record."
    };
  });
  const cityUpKey = "CTY-UPCOMING-FRM";
  const cityUpOv = job.p6StatusOverrides[cityUpKey] || {};
  cityRows.unshift({
    rowKey: cityUpKey,
    secKey: "city",
    badge: "PERMIT FEE",
    title: "District of Squamish — Stage 09 Framing, Plumbing & Occupancy Inspection Fee Schedule",
    dateISO: "2026-10-28",
    pdfName: job.jobId + "_Squamish_Framing_Inspection_Fee_Invoice.pdf",
    amount: (typeof cityUpOv.amount === "number") ? cityUpOv.amount : r(2400),
    paid: (typeof cityUpOv.paid === "boolean") ? cityUpOv.paid : false,
    paidDate: cityUpOv.paidDate || "",
    openPdfFn: `openP6MasterPdfItem('city', '${cityUpKey}')`,
    desc: "District of Squamish municipal inspection & permit compliance fee invoice for Stage 09 Rough Framing & Shear Wall sign-off (#" + (job.permitNum || "BP2026-0419") + ")."
  });
  (job.p6CustomEntries.city || []).forEach(c => cityRows.unshift(c));

  // 4. ARCHITECT (Live from job.datedVaultDocs.arch + Architectural Fee Invoices)
  const defaultArchAmounts = [r(4500), r(8500), r(6500), r(5500), r(32000), r(6000)];
  const archDocs = getSortedCategoryDocs(job, "arch");
  const archRows = archDocs.map((doc, idx) => {
    const rowKey = "ARC-DOC-" + doc.id;
    const ov = job.p6StatusOverrides[rowKey] || {};
    const defaultAmt = defaultArchAmounts[idx % defaultArchAmounts.length];
    const isPaid = (typeof ov.paid === "boolean") ? ov.paid : true;
    const amt = (typeof ov.amount === "number") ? ov.amount : defaultAmt;
    return {
      rowKey,
      secKey: "architect",
      badge: doc.code || "ARCHITECT PDF",
      title: doc.title,
      dateISO: doc.dateISO || "2026-10-12",
      pdfName: doc.pdfName,
      amount: amt,
      paid: isPaid,
      paidDate: ov.paidDate || doc.dateISO || "2026-10-12",
      openPdfFn: `openP6MasterPdfItem('architect', '${rowKey}')`,
      desc: doc.bodyText || doc.sub || "Official Studio Vance Architecture AIBC drawing & PDF record."
    };
  });
  const archUpKey = "ARC-CA-WALKTHROUGH";
  const archUpOv = job.p6StatusOverrides[archUpKey] || {};
  archRows.unshift({
    rowKey: archUpKey,
    secKey: "architect",
    badge: "AIBC RETAINER",
    title: "Studio Vance Architecture AIBC — Construction Field Review & Pre-Occupancy Sign-Off",
    dateISO: "2026-11-12",
    pdfName: job.jobId + "_Architect_Field_Review_Retainer_Invoice.pdf",
    amount: (typeof archUpOv.amount === "number") ? archUpOv.amount : r(6500),
    paid: (typeof archUpOv.paid === "boolean") ? archUpOv.paid : false,
    paidDate: archUpOv.paidDate || "",
    openPdfFn: `openP6MasterPdfItem('architect', '${archUpKey}')`,
    desc: "Architectural field review, window/envelope detailing inspection, and Letter of Assurance sign-off by Studio Vance Architecture AIBC."
  });
  (job.p6CustomEntries.architect || []).forEach(c => archRows.unshift(c));

  // 5. ENGINEER (Live from job.datedVaultDocs.eng + Structural & Geotech Engineering Fee Invoices)
  const defaultEngAmounts = [r(9500), r(4800), r(14200), r(4200), r(3800), r(5200)];
  const engDocs = getSortedCategoryDocs(job, "eng");
  const engRows = engDocs.map((doc, idx) => {
    const rowKey = "ENG-DOC-" + doc.id;
    const ov = job.p6StatusOverrides[rowKey] || {};
    const defaultAmt = defaultEngAmounts[idx % defaultEngAmounts.length];
    const isPaid = (typeof ov.paid === "boolean") ? ov.paid : true;
    const amt = (typeof ov.amount === "number") ? ov.amount : defaultAmt;
    return {
      rowKey,
      secKey: "engineer",
      badge: doc.code || "P.ENG. PDF",
      title: doc.title,
      dateISO: doc.dateISO || "2026-10-12",
      pdfName: doc.pdfName,
      amount: amt,
      paid: isPaid,
      paidDate: ov.paidDate || doc.dateISO || "2026-10-12",
      openPdfFn: `openP6MasterPdfItem('engineer', '${rowKey}')`,
      desc: doc.bodyText || doc.sub || "Official Structural & Geotechnical P.Eng. Schedule B record."
    };
  });
  const engUpKey = "ENG-SCHED-CB";
  const engUpOv = job.p6StatusOverrides[engUpKey] || {};
  engRows.unshift({
    rowKey: engUpKey,
    secKey: "engineer",
    badge: "SCHEDULE C-B",
    title: "Apex Structural & Geotech P.Eng. — Roof Truss, Shear Wall & Schedule C-B Assurance",
    dateISO: "2026-11-05",
    pdfName: job.jobId + "_Apex_Structural_Schedule_CB_Invoice.pdf",
    amount: (typeof engUpOv.amount === "number") ? engUpOv.amount : r(5500),
    paid: (typeof engUpOv.paid === "boolean") ? engUpOv.paid : false,
    paidDate: engUpOv.paidDate || "",
    openPdfFn: `openP6MasterPdfItem('engineer', '${engUpKey}')`,
    desc: "Sealed Structural Schedule B/C-B field review of roof truss bearing, HDU8 hold-downs, and shear wall nailing schedule."
  });
  (job.p6CustomEntries.engineer || []).forEach(c => engRows.unshift(c));

  return [
    { key: "trades",    label: "1. Trades — Subcontracts, Progress Draws & Change Order PDFs", items: tradeRows },
    { key: "materials", label: "2. Materials — Civil, Excavation, Concrete, Framing, Roofing, Siding & Finishing PDFs", items: materialRows },
    { key: "city",      label: "3. City (" + resolveJobMunicipality(job) + ") — Building Permit, Fees & Inspection PDFs", items: cityRows },
    { key: "architect", label: "4. Architect (AIBC) — Architectural Plans, Permit Set & Revision PDFs", items: archRows },
    { key: "engineer",  label: "5. Engineer (P.Eng.) — Structural, Geotechnical Schedule B & Field Review PDFs", items: engRows }
  ];
}

function renderTab6JobManager() {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const revStats = getJobSignedRevisionsSum(job);
  const revisedContract = (Number(job.contractPrice) || 0) + revStats.signedSum;

  const hBadge = document.getElementById("p6-highland-badge");
  if (hBadge) hBadge.innerText = "HIGHLAND MULTIPLEX • " + job.jobId;
  const mTitle = document.getElementById("p6-master-title");
  if (mTitle) mTitle.innerText = job.address + " — Keystone Master Financial & PDF Breakdown";

  let grandPaid = 0;
  let grandUnpaid = 0;
  let grandTotal = 0;
  let grandPaidCount = 0;
  let grandUnpaidCount = 0;

  const sectionSummaries = sections.map(sec => {
    let secPaid = 0;
    let secUnpaid = 0;
    let secPaidCnt = 0;
    let secUnpaidCnt = 0;
    sec.items.forEach(it => {
      const a = Number(it.amount) || 0;
      if (it.paid) {
        secPaid += a;
        grandPaid += a;
        secPaidCnt++;
        grandPaidCount++;
      } else {
        secUnpaid += a;
        grandUnpaid += a;
        secUnpaidCnt++;
        grandUnpaidCount++;
      }
      grandTotal += a;
    });
    return {
      key: sec.key,
      label: sec.label,
      count: sec.items.length,
      paid: secPaid,
      unpaid: secUnpaid,
      total: secPaid + secUnpaid,
      paidCnt: secPaidCnt,
      unpaidCnt: secUnpaidCnt
    };
  });

  const remainingContractFloat = Math.max(0, revisedContract - grandTotal);
  const pctCommitted = revisedContract > 0 ? ((grandTotal / revisedContract) * 100).toFixed(1) : "0.0";

  // Update Top 4-Card Keystone Master Breakdown
  const elContract = document.getElementById("p6-kpi-contract-total");
  const elContractSub = document.getElementById("p6-kpi-contract-sub");
  const elPaid = document.getElementById("p6-kpi-paid-total");
  const elPaidSub = document.getElementById("p6-kpi-paid-sub");
  const elUnpaid = document.getElementById("p6-kpi-unpaid-total");
  const elUnpaidSub = document.getElementById("p6-kpi-unpaid-sub");
  const elWhere = document.getElementById("p6-kpi-where-we-sit");
  const elRemSub = document.getElementById("p6-kpi-remaining-sub");

  if (elContract) elContract.innerText = fmtMoney(revisedContract);
  if (elContractSub) elContractSub.innerText = `Baseline ${fmtMoney(job.contractPrice)} + Revisions +${fmtMoney(revStats.signedSum)}`;
  if (elPaid) elPaid.innerText = fmtMoney(grandPaid);
  if (elPaidSub) elPaidSub.innerText = `${grandPaidCount} Paid PDFs Across All 5 Sections`;
  if (elUnpaid) elUnpaid.innerText = fmtMoney(grandUnpaid);
  if (elUnpaidSub) elUnpaidSub.innerText = `${grandUnpaidCount} Unpaid / Active PDFs Pending`;
  if (elWhere) elWhere.innerText = fmtMoney(grandTotal);
  if (elRemSub) elRemSub.innerText = `${pctCommitted}% Committed • ${fmtMoney(remainingContractFloat)} Remaining Float`;

  // Update 10% Statutory Builders Lien Holdback & CCDC 5B Summary Bar in Tab 6
  const hbGross = grandPaid > 0 ? grandPaid : grandTotal;
  const hb10Pct = Math.round(hbGross * 0.10);
  const hbNet90 = hbGross - hb10Pct;
  const hbCmFee = Math.round(hbGross * 0.125);
  const elHbGross = document.getElementById("p6-holdback-gross-val");
  const elHb10 = document.getElementById("p6-holdback-10pct-val");
  const elHbNet90 = document.getElementById("p6-holdback-net90-val");
  const elHbCm = document.getElementById("p6-holdback-cmfee-val");
  if (elHbGross) elHbGross.innerText = fmtMoney(hbGross);
  if (elHb10) elHb10.innerText = fmtMoney(hb10Pct);
  if (elHbNet90) elHbNet90.innerText = fmtMoney(hbNet90);
  if (elHbCm) elHbCm.innerText = fmtMoney(hbCmFee) + " (12.5%)";

  // Render the 5 Live Section Boxes (1. Trades, 2. Materials, 3. City, 4. Architect, 5. Engineer)
  const container = document.getElementById("p6-five-sections-container");
  if (container) {
    container.innerHTML = sections.map((sec, sIdx) => {
      const sum = sectionSummaries[sIdx];
      const rowsHtml = sec.items.map(it => {
        const invClick = it.openInvFn
          ? it.openInvFn
          : `openP6MasterInvoiceModal('${escapeHtml(sec.key)}', '${escapeHtml(it.rowKey)}')`;

        return `
          <div
            style="background:#05070b; border:1px solid ${it.paid ? "rgba(212,175,55,0.42)" : "rgba(255,255,255,0.16)"}; border-radius:10px; padding:9px 13px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; transition:all 0.15s ease;"
          >
            <!-- LEFT: Clickable PDF Document Row -->
            <div
              onclick="${it.openPdfFn}"
              style="display:flex; align-items:center; gap:10px; min-width:0; flex:1; cursor:pointer;"
              title="Click to open PDF on screen: ${escapeHtml(it.pdfName)}"
            >
              <span class="kp-badge-pill kp-badge-gold" style="min-width:74px; text-align:center;">
                ${escapeHtml(it.badge)}
              </span>
              <div style="min-width:0; flex:1;">
                <div style="font-size:0.85rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                  ${escapeHtml(it.title)}
                </div>
                <div style="font-size:0.7rem; color:#94a3b8; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                  PDF: <strong style="color:#cbd5e1;">${escapeHtml(it.pdfName)}</strong> &bull; Date: ${escapeHtml(it.dateISO)}
                </div>
              </div>
            </div>

            <!-- RIGHT: Amount + Paid / Not Paid Button (Opens Invoice / Payment Status PDF) -->
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span
                onclick="promptEditP6ItemAmount('${escapeHtml(sec.key)}', '${escapeHtml(it.rowKey)}')"
                style="font-size:0.88rem; font-weight:900; color:${it.paid ? "#d4af37" : "#ffffff"}; font-variant-numeric:tabular-nums; cursor:pointer;"
                title="Click to adjust dollar amount"
              >
                ${fmtMoney(it.amount)}
              </span>

              <button
                type="button"
                onclick="${invClick}"
                class="${it.paid ? "kp-gold-btn" : "kp-secondary-btn"} kp-pill-sm"
                style="min-width:132px; justify-content:center;"
                title="Click to open Invoice & Payment Record PDF (or toggle Paid / Unpaid)"
              >
                ${it.paid ? ("✓ PAID (" + escapeHtml(it.paidDate || it.dateISO) + ")") : "UNPAID"}
              </button>
            </div>
          </div>
        `;
      }).join("");

      return `
        <div style="background:#080c14; border:1px solid rgba(212,175,55,0.28); border-radius:12px; padding:13px 16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:9px; padding-bottom:7px; border-bottom:1px solid rgba(255,255,255,0.1);">
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.93rem; font-weight:900; color:#ffffff; letter-spacing:0.02em;">
                ${escapeHtml(sec.label)}
              </span>
              <span class="kp-badge-pill kp-badge-white">
                ${sum.count} PDFs
              </span>
            </div>

            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span style="font-size:0.75rem; color:#cbd5e1; font-weight:700;">
                Paid: <strong style="color:#d4af37;">${fmtMoney(sum.paid)}</strong>
                &bull; Unpaid: <strong style="color:#ffffff;">${fmtMoney(sum.unpaid)}</strong>
                &bull; Section Total: <strong style="color:#f3e5ab;">${fmtMoney(sum.total)}</strong>
              </span>
              <button type="button" onclick="promptAddMasterFinancialEntry('${escapeHtml(sec.key)}')" class="kp-secondary-btn kp-pill-sm">
                + Add PDF / Entry
              </button>
            </div>
          </div>

          <!-- Scrollable PDF List Inside Each of the 5 Sections -->
          <div style="display:flex; flex-direction:column; gap:6px; max-height:215px; overflow-y:auto; padding-right:2px;">
            ${rowsHtml}
          </div>
        </div>
      `;
    }).join("");
  }

  // Render Bottom Highland Master Tally (Paid, Unpaid & How Much We Are At)
  const tallyBox = document.getElementById("p6-bottom-master-tally-box");
  if (tallyBox) {
    tallyBox.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:9px; border-bottom:1px solid rgba(212,175,55,0.35);">
        <div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span class="kp-badge-pill kp-badge-gold">HIGHLAND MULTIPLEX MASTER TALLY</span>
            <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:1.02rem; font-weight:900; color:#ffffff;">
              ${escapeHtml(job.address)} &mdash; Paid, Unpaid &amp; Where We Sit Tally
            </span>
          </div>
          <div style="font-size:0.74rem; color:#cbd5e1; margin-top:3px;">
            Live financial rollup across Trades, Materials, City, Architect, and Engineer PDFs against the ${fmtMoney(revisedContract)} Revised Contract.
          </div>
        </div>
        <button type="button" onclick="exportHighlandMasterFinancialPdf()" class="kp-gold-btn kp-pill-sm">
          Open &amp; Print Master Tally PDF
        </button>
      </div>

      <!-- 5-Section Breakdown Rows -->
      <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:14px;">
        ${sectionSummaries.map(s => `
          <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.12); border-radius:9px; padding:8px 13px; display:grid; grid-template-columns:minmax(0, 1.8fr) repeat(3, minmax(110px, 0.7fr)); align-items:center; gap:10px; font-size:0.8rem;">
            <div style="font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
              ${escapeHtml(s.label)} <span style="color:#94a3b8; font-weight:600;">(${s.count} PDFs)</span>
            </div>
            <div style="text-align:right; color:#cbd5e1;">
              Paid: <strong style="color:#d4af37;">${fmtMoney(s.paid)}</strong>
            </div>
            <div style="text-align:right; color:#cbd5e1;">
              Unpaid: <strong style="color:#ffffff;">${fmtMoney(s.unpaid)}</strong>
            </div>
            <div style="text-align:right; color:#f3e5ab; font-weight:900;">
              Total: ${fmtMoney(s.total)}
            </div>
          </div>
        `).join("")}
      </div>

      <!-- Bottom Grand Total Bar: Total Paid | Total Unpaid | How Much We Are At | Remaining Contract Float -->
      <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:10px; background:linear-gradient(180deg, rgba(212,175,55,0.12) 0%, #080c14 100%); border:1.5px solid #d4af37; border-radius:12px; padding:12px 15px;">
        <div>
          <div style="font-size:0.66rem; font-weight:800; color:#f3e5ab; text-transform:uppercase; letter-spacing:0.06em;">1. Total Paid (All PDFs)</div>
          <div style="font-size:1.32rem; font-weight:900; color:#d4af37; margin-top:2px;">${fmtMoney(grandPaid)}</div>
          <div style="font-size:0.7rem; color:#cbd5e1;">${grandPaidCount} Verified Paid Invoices &amp; Draws</div>
        </div>
        <div>
          <div style="font-size:0.66rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">2. Total Unpaid (Pending)</div>
          <div style="font-size:1.32rem; font-weight:900; color:#ffffff; margin-top:2px;">${fmtMoney(grandUnpaid)}</div>
          <div style="font-size:0.7rem; color:#94a3b8;">${grandUnpaidCount} Open / Upcoming PDFs</div>
        </div>
        <div>
          <div style="font-size:0.66rem; font-weight:800; color:#f3e5ab; text-transform:uppercase; letter-spacing:0.06em;">3. How Much We Are At (Paid + Unpaid)</div>
          <div style="font-size:1.32rem; font-weight:900; color:#ffffff; margin-top:2px;">${fmtMoney(grandTotal)}</div>
          <div style="font-size:0.7rem; color:#f3e5ab;">${pctCommitted}% of ${fmtMoney(revisedContract)} Highland Contract</div>
        </div>
        <div>
          <div style="font-size:0.66rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">4. Remaining Contract Float</div>
          <div style="font-size:1.32rem; font-weight:900; color:#d4af37; margin-top:2px;">${fmtMoney(remainingContractFloat)}</div>
          <div style="font-size:0.7rem; color:#cbd5e1;">Unallocated Stages 15–30 Balance</div>
        </div>
      </div>
    `;
  }
}

function openP6MasterPdfItem(secKey, rowKey) {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const sec = sections.find(s => s.key === secKey);
  if (!sec) return;
  const item = sec.items.find(x => x.rowKey === rowKey);
  if (!item) return;

  openCustomVaultPdfOnScreen(
    item.title,
    item.pdfName,
    sec.label + " • Date: " + item.dateISO + " • Amount: " + fmtMoney(item.amount) + " (" + (item.paid ? "PAID ✓" : "UNPAID") + ")",
    [
      "HIGHLAND MULTIPLEX (" + job.jobId + ") — " + job.address,
      "SECTION: " + sec.label.toUpperCase(),
      "DOCUMENT / RECORD: " + item.title,
      "PDF FILE: " + item.pdfName + " | DATE: " + item.dateISO,
      "AMOUNT: " + fmtMoney(item.amount) + " | STATUS: " + (item.paid ? ("PAID ON " + (item.paidDate || item.dateISO)) : "UNPAID / PENDING"),
      "------------------------------------------------------------------------",
      item.desc || "Official verified project PDF & financial record."
    ].join("\n\n"),
    item.dataUrl || ""
  );
}

function openP6MasterInvoiceModal(secKey, rowKey) {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const sec = sections.find(s => s.key === secKey);
  if (!sec) return;
  const item = sec.items.find(x => x.rowKey === rowKey);
  if (!item) return;

  const modal = document.getElementById("modal-pdf-viewer");
  const titleEl = document.getElementById("pdf-modal-title");
  const bodyEl = document.getElementById("pdf-modal-body");
  const dlBtn = document.getElementById("pdf-modal-download-btn");
  if (!modal || !bodyEl) return;

  if (titleEl) {
    titleEl.innerText = "Invoice & Payment Status — " + item.title;
  }

  const pdfLines = [
    "HIGHLAND MULTIPLEX — MASTER FINANCIAL & INVOICE RECORD",
    "SECTION: " + sec.label.toUpperCase(),
    "ITEM: " + item.title,
    "PDF FILE: " + item.pdfName + " | DATE: " + item.dateISO,
    "INVOICE AMOUNT: " + fmtMoney(item.amount),
    "PAYMENT STATUS: " + (item.paid ? ("PAID IN FULL ✓ — PAID ON " + (item.paidDate || item.dateISO)) : "UNPAID / OUTSTANDING"),
    "------------------------------------------------------------------------",
    item.desc || "Verified Highland Multiplex invoice & payment record."
  ];

  if (dlBtn) {
    dlBtn.innerText = "Download Invoice PDF";
    dlBtn.onclick = () => triggerDummyDownload(item.pdfName, pdfLines.join("\n"));
  }

  bodyEl.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; background:#0b0f17; border:1px solid rgba(212,175,55,0.45); border-radius:9999px; padding:8px 16px; margin:0 auto 16px auto; max-width:850px;">
      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <span class="kp-badge-pill ${item.paid ? "kp-badge-gold" : "kp-badge-white"}">
          ${item.paid ? ("✓ PAID — PAID ON " + escapeHtml(item.paidDate || item.dateISO)) : "STATUS: UNPAID"}
        </span>
        <span style="font-size:0.78rem; color:#ffffff; font-weight:800;">
          Amount: ${fmtMoney(item.amount)}
        </span>
      </div>
      <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
        <button
          type="button"
          onclick="toggleP6MasterItemPaid('${escapeHtml(secKey)}', '${escapeHtml(rowKey)}')"
          class="${item.paid ? "kp-secondary-btn" : "kp-gold-btn"} kp-pill-sm"
        >
          ${item.paid ? "Mark as Unpaid" : "✓ Mark Paid Today"}
        </button>
        <button type="button" onclick="window.print()" class="kp-secondary-btn kp-pill-sm">Print PDF</button>
      </div>
    </div>

    <div class="kp-pdf-page-sheet">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:3px solid #0f172a; padding-bottom:16px; margin-bottom:18px;">
        <div>
          <div style="font-size:0.72rem; font-weight:800; letter-spacing:0.1em; color:#b45309; text-transform:uppercase;">
            ${escapeHtml(sec.label)}
          </div>
          <h2 style="font-size:1.32rem; font-weight:900; color:#0f172a; margin:4px 0 2px 0; font-family:'Outfit','Plus Jakarta Sans',sans-serif;">
            ${escapeHtml(item.title)}
          </h2>
          <div style="font-size:0.82rem; font-weight:700; color:#334155;">
            PDF File: ${escapeHtml(item.pdfName)}
          </div>
        </div>
        <div style="text-align:right;">
          <div style="background:${item.paid ? "#0f172a" : "#7f1d1d"}; color:${item.paid ? "#d4af37" : "#ffffff"}; font-weight:900; font-size:0.76rem; padding:6px 12px; border-radius:4px;">
            ${item.paid ? ("✓ PAID • " + escapeHtml(item.paidDate || item.dateISO)) : "UNPAID"}
          </div>
          <div style="font-size:0.74rem; color:#475569; margin-top:5px;">
            Document Date: <strong>${escapeHtml(item.dateISO)}</strong>
          </div>
        </div>
      </div>

      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:6px; padding:12px 16px; margin-bottom:18px; display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; font-size:0.8rem;">
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Payment Status</div>
          <div style="font-size:0.92rem; font-weight:900; color:#0f172a; margin-top:2px;">
            ${item.paid ? "PAID OFF ✓" : "UNPAID / PENDING"}
          </div>
        </div>
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Date Paid</div>
          <div style="font-size:0.92rem; font-weight:900; color:#0f172a; margin-top:2px;">
            ${item.paid ? escapeHtml(item.paidDate || item.dateISO) : "Not Paid Yet"}
          </div>
        </div>
        <div>
          <div style="font-size:0.68rem; font-weight:800; color:#64748b; text-transform:uppercase;">Invoice Total</div>
          <div style="font-size:0.98rem; font-weight:900; color:#0f172a; margin-top:2px;">
            ${fmtMoney(item.amount)}
          </div>
        </div>
      </div>

      <p style="font-size:0.85rem; line-height:1.65; color:#1e293b !important;">
        ${escapeHtml(item.desc || "Official verified Highland Multiplex financial and PDF record.")}
      </p>
    </div>
  `;

  modal.classList.add("open");
  modal.style.display = "flex";
}

function toggleP6MasterItemPaid(secKey, rowKey) {
  const job = getActiveJob();
  ensureMasterFinancialLedgerVault(job);
  const todayISO = job.whereWeAreDate || "2026-10-17";

  // Check if it's a custom entry first
  const custList = job.p6CustomEntries[secKey] || [];
  const custItem = custList.find(x => x.rowKey === rowKey);
  if (custItem) {
    custItem.paid = !custItem.paid;
    custItem.paidDate = custItem.paid ? todayISO : "";
  } else {
    const cur = job.p6StatusOverrides[rowKey] || {};
    const sections = collectHighland5SectionsData(job);
    const sec = sections.find(s => s.key === secKey);
    const existing = sec ? sec.items.find(x => x.rowKey === rowKey) : null;
    const nextPaid = existing ? !existing.paid : !cur.paid;
    job.p6StatusOverrides[rowKey] = Object.assign({}, cur, {
      paid: nextPaid,
      paidDate: nextPaid ? todayISO : ""
    });
  }

  saveState();
  renderTab6JobManager();
  openP6MasterInvoiceModal(secKey, rowKey);
  showToast("Updated Paid / Unpaid status & live Highland Master Tally");
}

function promptEditP6ItemAmount(secKey, rowKey) {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const sec = sections.find(s => s.key === secKey);
  if (!sec) return;
  const item = sec.items.find(x => x.rowKey === rowKey);
  if (!item) return;

  const val = prompt("Update Dollar Amount ($ CAD) for " + item.title + ":", String(item.amount || 0));
  if (val === null) return;
  const num = Number(String(val).replace(/[^0-9.]/g, ""));
  if (isNaN(num)) return;

  if (item.matSecKey && item.matPkgId) {
    const list = job.materialSectionsVault[item.matSecKey] || [];
    const pkg = list.find(x => String(x.id) === String(item.matPkgId));
    if (pkg) {
      pkg.baseCost = job.costPlus10Enabled ? Math.round(num / 1.10) : num;
    }
  } else {
    const custList = job.p6CustomEntries[secKey] || [];
    const custItem = custList.find(x => x.rowKey === rowKey);
    if (custItem) {
      custItem.amount = num;
    } else {
      job.p6StatusOverrides[rowKey] = Object.assign({}, job.p6StatusOverrides[rowKey] || {}, { amount: num });
    }
  }

  saveState();
  renderMaterialsList();
  renderTab6JobManager();
  showToast("Updated amount to " + fmtMoney(num) + " — Master Tally recalculated");
}

function promptAddMasterFinancialEntry(defaultSecKey) {
  const job = getActiveJob();
  ensureMasterFinancialLedgerVault(job);
  let secKey = defaultSecKey;
  if (!secKey) {
    const pick = prompt("Which section is this PDF / Financial entry for?\n1 = Trades\n2 = Materials\n3 = City\n4 = Architect\n5 = Engineer", "1");
    if (!pick) return;
    const map = { "1": "trades", "2": "materials", "3": "city", "4": "architect", "5": "engineer" };
    secKey = map[String(pick).trim()] || "trades";
  }

  const title = prompt("Enter Title / Description for this PDF & Financial Entry:", "Additional Highland Multiplex Invoice & PDF");
  if (!title) return;
  const amtStr = prompt("Enter Total Amount ($ CAD):", "6500");
  if (amtStr === null) return;
  const amt = Number(String(amtStr).replace(/[^0-9.]/g, "")) || 0;
  const paidAns = confirm("Has this invoice already been PAID?\nClick OK for PAID, or Cancel for UNPAID.");
  const todayISO = job.whereWeAreDate || "2026-10-17";
  const rowKey = "CUST-" + secKey.toUpperCase() + "-" + Date.now().toString().slice(-4);
  const cleanFile = title.trim().replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 36);

  job.p6CustomEntries[secKey] = job.p6CustomEntries[secKey] || [];
  job.p6CustomEntries[secKey].unshift({
    rowKey,
    secKey,
    badge: secKey.toUpperCase(),
    title: title.trim(),
    dateISO: todayISO,
    pdfName: `${job.jobId}_${cleanFile}.pdf`,
    amount: amt,
    paid: paidAns,
    paidDate: paidAns ? todayISO : "",
    openPdfFn: `openP6MasterPdfItem('${secKey}', '${rowKey}')`,
    desc: `Custom financial & PDF record added under ${secKey.toUpperCase()} for ${job.address}.`
  });

  saveState();
  renderTab6JobManager();
  showToast(`Added ${title.trim()} (${fmtMoney(amt)}) under ${secKey.toUpperCase()}`);
}

function exportHighlandMasterFinancialPdf() {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const revStats = getJobSignedRevisionsSum(job);
  const revisedContract = (Number(job.contractPrice) || 0) + revStats.signedSum;

  let grandPaid = 0;
  let grandUnpaid = 0;
  const lines = [
    "HIGHLAND MULTIPLEX (" + job.jobId + ") — KEYSTONE MASTER FINANCIAL & PDF LEDGER",
    "PROJECT ADDRESS: " + job.address + " | PERMIT #" + (job.permitNum || "BP2026-0419"),
    "REVISED CONTRACT TOTAL: " + fmtMoney(revisedContract) + " (Baseline " + fmtMoney(job.contractPrice) + " + Revisions +" + fmtMoney(revStats.signedSum) + ")",
    "========================================================================"
  ];

  sections.forEach(sec => {
    let secPaid = 0;
    let secUnpaid = 0;
    lines.push(sec.label.toUpperCase());
    sec.items.forEach(it => {
      const a = Number(it.amount) || 0;
      if (it.paid) { secPaid += a; grandPaid += a; }
      else { secUnpaid += a; grandUnpaid += a; }
      lines.push(`  - [${it.paid ? "PAID" : "UNPAID"}] ${it.title} | ${fmtMoney(a)} | PDF: ${it.pdfName}`);
    });
    lines.push(`  SECTION SUBTOTAL — Paid: ${fmtMoney(secPaid)} | Unpaid: ${fmtMoney(secUnpaid)} | Total: ${fmtMoney(secPaid + secUnpaid)}`);
    lines.push("------------------------------------------------------------------------");
  });

  const grandTotal = grandPaid + grandUnpaid;
  lines.push("GRAND TALLY — PAID: " + fmtMoney(grandPaid) + " | UNPAID: " + fmtMoney(grandUnpaid));
  lines.push("HOW MUCH WE ARE AT (TOTAL COMMITTED): " + fmtMoney(grandTotal) + " | REMAINING CONTRACT FLOAT: " + fmtMoney(Math.max(0, revisedContract - grandTotal)));

  const pdfFile = job.jobId + "_Highland_Master_Financial_And_PDF_Tally.pdf";
  triggerDummyDownload(pdfFile, lines.join("\n"));
  showToast("Downloaded Highland Master Financial & PDF Tally: " + pdfFile);
}

function saveJobSettingsFromTab6() {
  renderTab6JobManager();
}


async function syncAllJobsToServerAndHub(silent) {
  try {
    localStorage.setItem(LS_MULTI_KEY, JSON.stringify(portalStore));
  } catch (e) {}
  const statusEl = document.getElementById("p6-sync-status-text");
  if (statusEl && !silent) statusEl.innerText = "Syncing Job Portal ledger to Keystone Cloud Vault...";

  const jobsDict = {};
  (portalStore.jobs || []).forEach(j => {
    const jid = j.jobId || j.job_id || "KP-2026-001";
    jobsDict[jid] = Object.assign({ job_id: jid, jobId: jid }, j);
  });
  const payload = {
    activeJobId: portalStore.activeJobId,
    jobs: jobsDict
  };

  // Sync to hardened WordPress REST endpoint with Builder Session Header
  try {
    const authHdrs = getBuilderAuthHeaders();
    if (authHdrs["X-KP-Builder-Session"] || authHdrs["X-WP-Nonce"]) {
      await fetch("/wp-json/keystone/v1/portal-jobs", {
        method: "POST",
        headers: authHdrs,
        body: JSON.stringify(payload)
      });
    }
  } catch (e) {}

  const stamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  if (statusEl) {
    statusEl.innerHTML = `✓ <strong style="color:#d4af37;">Synced ${portalStore.jobs.length} Job Portal(s)</strong> to Browser Vault &amp; Keystone Cloud Server at ${stamp}.`;
  }
  if (!silent) showToast("Synced Job Portal ledger to Keystone Cloud Vault");
}

async function deletePortalJobFromServer(jobId) {
  if (!jobId) return false;
  try {
    const resp = await fetch("/wp-json/keystone/v1/portal-jobs", {
      method: "DELETE",
      headers: getBuilderAuthHeaders(),
      body: JSON.stringify({ jobId: jobId, job_id: jobId })
    });
    return resp.ok;
  } catch (e) {
    return false;
  }
}
window.deletePortalJobFromServer = deletePortalJobFromServer;

async function hydrateFromWordPressServer() {
  try {
    const jobsEndpoint = (window.kpPortalConfig && window.kpPortalConfig.jobsUrl) || "/wp-json/keystone/v1/portal-jobs";
    const sep = jobsEndpoint.indexOf("?") >= 0 ? "&" : "?";
    const r = await fetch(jobsEndpoint + sep + "t=" + Date.now(), {
      headers: getBuilderAuthHeaders()
    });
    if (!r.ok) return;
    const data = await r.json();
    if (data && data.jobs && typeof data.jobs === "object") {
      const serverJobs = Object.values(data.jobs).filter(j => j && (j.jobId || j.job_id || j.id));
      if (serverJobs.length > 0) {
        const byId = {};
        (portalStore.jobs || []).forEach(j => { byId[j.jobId] = j; });
        serverJobs.forEach(sj => {
          const jid = sj.jobId || sj.job_id || sj.id;
          sj.jobId = jid;
          if (!byId[jid]) {
            portalStore.jobs.push(sj);
          } else if (sj.ownerPasscode || sj.builderPasscode) {
            byId[jid].ownerPasscode = sj.ownerPasscode || byId[jid].ownerPasscode || "";
            if (sj.builderPasscode) byId[jid].builderPasscode = sj.builderPasscode;
          }
        });
        renderJobSelectors();
        renderTab6JobManager();
      } else if (data.authenticated) {
        syncAllJobsToServerAndHub(true);
      }
    }
  } catch (e) {}
}

function exportProjectJSON() {
  const blob = new Blob([JSON.stringify(portalStore, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "Keystone_MultiJob_Portal_Backup_v10.json";
  a.click();
}

function exportLedgerCSV() {
  exportTradesSummary();
}

function printExecutiveLedger() {
  window.print();
}

function resetPortalDemoData() {
  if (!confirm("Reset all Job Portals back to the 3 factory pre-seeded jobs?")) return;
  localStorage.removeItem(LS_MULTI_KEY);
  portalStore = loadMultiJobStore();
  renderAllPortalComponents();
  showToast("↺ Restored Factory Multi-Job Portal Data");
}

function openExecutiveBinderModal() {
  const job = getActiveJob();
  const grid = document.getElementById("contacts-grid");
  if (grid) {
    grid.innerHTML = (job.contacts || []).map(c => `
      <div style="background:rgba(4,8,16,0.88); border:1px solid rgba(56,189,248,0.35); border-radius:12px; padding:12px;">
        <div style="font-size:0.7rem; font-weight:800; color:#d4af37; text-transform:uppercase;">${escapeHtml(c.role)}</div>
        <div style="font-size:0.9rem; font-weight:800; color:#ffffff; margin-top:2px;">${escapeHtml(c.name)}</div>
        <div style="font-size:0.75rem; color:#38bdf8;">${escapeHtml(c.license)}</div>
        <div style="font-size:0.75rem; color:#cbd5e1; margin-top:4px;">📞 ${escapeHtml(c.phone)}<br>✉️ ${escapeHtml(c.email)}</div>
      </div>
    `).join("");
  }
  openModal("modal-binder");
}

function openAddContactPrompt() {
  const job = getActiveJob();
  const role = prompt("Enter Authority Role (e.g. Envelope Engineer):");
  if (!role) return;
  const name = prompt("Enter Full Name:") || "Project Specialist";
  const phone = prompt("Enter Phone:") || "(604) 555-0100";
  job.contacts.push({ id: Date.now(), role, name, license: "Verified Authority", phone, email: "contact@keystonepossibilities.ca" });
  saveState();
  openExecutiveBinderModal();
}

function renderAllPortalComponents() {
  renderJobSelectors();
  initSignaturePadCanvas();
  renderTab1Contract();
  renderWhereWeAreBar();
  renderCalendar();
  renderActiveTradeRadar();
  renderWarrantyAndPlansTab();
  renderSheetList();
  renderActiveBlueprint();
  renderTradesList();
  calculateSmartTakeoff();
  renderMaterialsList();
  renderTab6JobManager();
  if (typeof renderTab7ThirtyStagesAndGeotech === "function") {
    renderTab7ThirtyStagesAndGeotech();
  }
}

window.switchPortalPage = switchPortalPage;
window.launchDemoProject = launchDemoProject;
window.handlePortalLogin = handlePortalLogin;
window.verifyPortalLogin = handlePortalLogin;
window.lockPortalSession = lockPortalSession;
window.switchActiveJob = switchActiveJob;
window.syncAllJobsToServerAndHub = syncAllJobsToServerAndHub;

try { renderAllPortalComponents(); } catch (e) { console.error("Initial render error:", e); }
document.addEventListener("DOMContentLoaded", () => {
  try { renderAllPortalComponents(); } catch (e) { console.error(e); }
});
setTimeout(() => {
  try {
    renderAllPortalComponents();
    hydrateFromWordPressServer();
  } catch (e) { console.error(e); }
}, 120);



// ============================================================================
// 10. TAB 7: 30-STAGE MASTER CHECKLIST, GEOTECHNICAL & 6-DISCIPLINE P.ENG,
//     BCBC 2024 LETTERS OF ASSURANCE, SIDE-BY-SIDE PLAN DIFF & CLOUD VAULT SYNC
// ============================================================================

const CANONICAL_30_STAGES_MASTER = [
  // Phase I: Pre-Construction, Survey, Arch, Geotech/6-Discipline P.Eng & Permits (01-05)
  { code: "ST-01", num: 1, phase: 1, phaseLabel: "Phase I: Pre-Con & Eng", name: "BCLS Legal Survey, Pinning & Topographic Benchmarks", trade: "Target Land Surveying (BCLS)", csi: "02-21-13", preds: [], baseBudget: 14500, defaultStatus: "Completed", gate: "BCLS Sealed Topographic & Geodetic Benchmark Plan Filed" },
  { code: "ST-02", num: 2, phase: 1, phaseLabel: "Phase I: Pre-Con & Eng", name: "Architect AIBC Schematic, DP & Bill 44 Multiplex Design", trade: "Studio Vance Architecture AIBC", csi: "01-11-00", preds: ["ST-01"], baseBudget: 68000, defaultStatus: "Completed", gate: "AIBC Sealed DP & Building Permit Drawings (Sheets A-101..A-401)" },
  { code: "ST-03", num: 3, phase: 1, phaseLabel: "Phase I: Pre-Con & Eng", name: "Geotechnical Investigation & 6-Discipline P.Eng Sealed Drawings", trade: "Thurber Geotech & Apex Structural P.Eng.", csi: "01-41-00", preds: ["ST-02"], baseBudget: 54000, defaultStatus: "Completed", gate: "Geotech Borehole/Bedrock Report + 6-Discipline Schedule B Filed" },
  { code: "ST-04", num: 4, phase: 1, phaseLabel: "Phase I: Pre-Con & Eng", name: "Energy Advisor BC Step Code 4 & Zero Carbon EL-4 Modeling", trade: "Sea-to-Sky Energy Advisors (NRCan)", csi: "01-41-19", preds: ["ST-03"], baseBudget: 9500, defaultStatus: "Completed", gate: "HOT2000 Pre-Construction Step Code 4 Compliance Dossier" },
  { code: "ST-05", num: 5, phase: 1, phaseLabel: "Phase I: Pre-Con & Eng", name: "Municipal Building Permits, BC Housing #52603 & 2-5-10 Warranty", trade: "Keystone Possibilities Ltd. (#52603)", csi: "01-41-26", preds: ["ST-04"], baseBudget: 42000, defaultStatus: "Completed", gate: "Municipal Building Permit #BP2026-0419 + NHW 2-5-10 Enrollment" },

  // Phase II: Abatement, Rock Excavation, Geotech Shoring, Civil ES54 & 35 MPa Concrete (06-11)
  { code: "ST-06", num: 6, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Hazardous Materials Abatement, Tree Hoarding & Site Clearing", trade: "Squamish Environmental & Demo", csi: "02-41-16", preds: ["ST-05"], baseBudget: 24000, defaultStatus: "Completed", gate: "WorkSafeBC Notice of Project & Arborist Tree Protection Sign-Off" },
  { code: "ST-07", num: 7, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Bulk Excavation, Rock Blasting & Geotechnical Shoring/Anchors", trade: "Tantalus Excavation & Thurber Geotech", csi: "31-23-16", preds: ["ST-06"], baseBudget: 88000, defaultStatus: "Completed", gate: "Geotechnical P.Eng Schedule B Subgrade (>300 kPa Bedrock) & Rock Dowels" },
  { code: "ST-08", num: 8, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Civil Utilities, Storm Detention, Sanitary & BC Hydro ES54 Ducts", trade: "Tantalus Civil & Underground Ltd.", csi: "33-11-00", preds: ["ST-07"], baseBudget: 64000, defaultStatus: "Completed", gate: "Civil P.Eng & Municipal Underground Servicing + BC Hydro ES54 Pass" },
  { code: "ST-09", num: 9, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Doka Formwork, 15M/20M Seismic Rebar & 35 MPa Footings/Walls", trade: "Garibaldi Concrete Forming Ltd.", csi: "03-30-00", preds: ["ST-08"], baseBudget: 138000, defaultStatus: "Completed", gate: "Structural P.Eng Schedule B Pre-Pour Rebar, Anchor Bolt & Cylinder Break" },
  { code: "ST-10", num: 10, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Elastomeric Waterproofing, Drain Tile & Geotech 98% Proctor Backfill", trade: "Pacific Envelope & Waterproofing", csi: "07-11-00", preds: ["ST-09"], baseBudget: 36000, defaultStatus: "Completed", gate: "Municipal Weeping Tile Inspection + Geotech 98% SPD Compaction Memo" },
  { code: "ST-11", num: 11, phase: 2, phaseLabel: "Phase II: Geotech, Civil & Found", name: "Under-Slab Plumbing, Geotech Subgrade, Radon Rock/Pipe & Slab Pour", trade: "Garibaldi Concrete & Sea-to-Sky Plumbing", csi: "03-35-00", preds: ["ST-10"], baseBudget: 52000, defaultStatus: "Completed", gate: "Plumbing Under-Slab DWV Pressure Test + 15-Mil Stego Wrap & Radon Seal" },

  // Phase III: Structural Steel, Rough Framing (#52603), Roofing, Windows & Envelope (12-16)
  { code: "ST-12", num: 12, phase: 3, phaseLabel: "Phase III: Superstructure & Envelope", name: "Structural Steel W-Beams, HSS Columns & Moment Frame Welding", trade: "Cascade Structural Steel Ltd.", csi: "05-12-00", preds: ["ST-11"], baseBudget: 74000, defaultStatus: "Completed", gate: "CWB Welding Certification + Structural P.Eng Moment Connection Field Memo" },
  { code: "ST-13", num: 13, phase: 3, phaseLabel: "Phase III: Superstructure & Envelope", name: "Rough Wood Framing, TJI Joists & Dick's Lumber #52603 Roof Trusses", trade: "Pacific Ridge Timberworks & Dick's Lumber", csi: "06-11-00", preds: ["ST-12"], baseBudget: 195000, defaultStatus: "Active On-Site", gate: "Structural P.Eng Simpson ATS Hold-Down, Shearwall & Truss Bracing Review" },
  { code: "ST-14", num: 14, phase: 3, phaseLabel: "Phase III: Superstructure & Envelope", name: "SBS Modified Bitumen Membrane & Standing-Seam Metal Roofing", trade: "Whistler Alpine Roofing Ltd.", csi: "07-52-00", preds: ["ST-13"], baseBudget: 68000, defaultStatus: "Scheduled", gate: "RCABC / Building Envelope P.Eng Roof Membrane & Flashing Inspection" },
  { code: "ST-15", num: 15, phase: 3, phaseLabel: "Phase III: Superstructure & Envelope", name: "NAFS European Triple-Glazed Windows & Lift-Slide Exterior Doors", trade: "EuroLine / Westcoast Fenestration", csi: "08-51-00", preds: ["ST-14"], baseBudget: 96000, defaultStatus: "Scheduled", gate: "NAFS Air/Water/Structural Label Verification & Envelope Sill Pan Review" },
  { code: "ST-16", num: 16, phase: 3, phaseLabel: "Phase III: Superstructure & Envelope", name: "SIGA Rainscreen WRB, Exterior Rockwool & Mid-Build Blower Door Test", trade: "Pacific Envelope & Energy Advisor", csi: "07-27-00", preds: ["ST-15"], baseBudget: 58000, defaultStatus: "Scheduled", gate: "Mid-Construction Blower Door Test (<= 1.0 ACH50 Step Code 4 Gate)" },

  // Phase IV: Parallel MEP Rough-Ins, Fire Sprinklers, Acoustic Insulation & Drywall (17-22)
  { code: "ST-17", num: 17, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "PEX-a Domestic Plumbing, Natural Gas & Hydronic Floor Rough-In", trade: "Sea-to-Sky Mechanical & Plumbing", csi: "22-11-00", preds: ["ST-16"], baseBudget: 76000, defaultStatus: "Scheduled", gate: "Municipal Plumbing & 100 PSI Hydronic Manifold Pressure Test" },
  { code: "ST-18", num: 18, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "Cold-Climate Heat Pumps, Zehnder HRV (88% SRE) & Sheet Metal Ducts", trade: "Coastal Climate HVAC Systems", csi: "23-05-00", preds: ["ST-16"], baseBudget: 84000, defaultStatus: "Scheduled", gate: "Mechanical P.Eng Schedule B Duct Sizing & Heat Pump Refrigerant Line Test" },
  { code: "ST-19", num: 19, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "NFPA 13D/13R Residential Fire Suppression Sprinklers & Hydro Test", trade: "Pacific Guard Fire Protection", csi: "21-13-00", preds: ["ST-16"], baseBudget: 38000, defaultStatus: "Scheduled", gate: "200 PSI 2-Hour Hydrostatic Fire Sprinkler Test & Fire Dept Sign-Off" },
  { code: "ST-20", num: 20, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "Electrical 400A Underground Service, EVEMS Chargers & Low-Voltage", trade: "Howe Sound Electrical Contractors", csi: "26-05-00", preds: ["ST-16"], baseBudget: 86000, defaultStatus: "Scheduled", gate: "Technical Safety BC Rough-In Electrical & EVEMS Load Management Pass" },
  { code: "ST-21", num: 21, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "Roxul Mineral Wool, STC 55+ Party-Wall Acoustic & Smart Vapour Barrier", trade: "Alpine Thermal & Acoustic Insulation", csi: "07-21-00", preds: ["ST-17", "ST-18", "ST-19", "ST-20"], baseBudget: 46000, defaultStatus: "Scheduled", gate: "Municipal Insulation, Acoustic Resilient Channel & Air/Vapour Inspection" },
  { code: "ST-22", num: 22, phase: 4, phaseLabel: "Phase IV: MEP, Fire & Drywall", name: "5/8\" Type X Fire-Rated Drywall, Acoustic Sealant & Level 5 Finish", trade: "Pinnacle Drywall & Plastering", csi: "09-29-00", preds: ["ST-21"], baseBudget: 78000, defaultStatus: "Scheduled", gate: "1-Hour Fire-Separation Continuity & Skim-Coat Moisture Check (<10%)" },

  // Phase V: Exterior Cladding, Interior Millwork, Tile/Hardwood & MEP Commissioning (23-28)
  { code: "ST-23", num: 23, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "Architectural Fibre-Cement, Clear Western Red Cedar & Soffit Cladding", trade: "Westcoast Rainscreen Cladding Ltd.", csi: "07-46-00", preds: ["ST-22"], baseBudget: 92000, defaultStatus: "Scheduled", gate: "Building Envelope P.Eng 3/4\" Rainscreen Cavity & Bug-Screen Sign-Off" },
  { code: "ST-24", num: 24, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "Solid-Core Interior Doors, Reveal Baseboards & Steel/Oak Stairs", trade: "Squamish Fine Finishing Carpentry", csi: "06-20-00", preds: ["ST-22"], baseBudget: 54000, defaultStatus: "Scheduled", gate: "BCBC Guardrail/Handrail Geometry & Architectural Reveal Tolerance Check" },
  { code: "ST-25", num: 25, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "Custom European Millwork Cabinetry & Bookmatched Quartz Countertops", trade: "Nordic Bespoke Millwork & Stone", csi: "12-35-00", preds: ["ST-24"], baseBudget: 88000, defaultStatus: "Scheduled", gate: "Laser-Templated Waterfall Quartz & Blum Hardware Alignment Sign-Off" },
  { code: "ST-26", num: 26, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "Schluter Kerdi Waterproofing, Large-Format Porcelain & White Oak Floors", trade: "Artisan Tile & Hardwood Surfaces", csi: "09-30-00", preds: ["ST-25"], baseBudget: 74000, defaultStatus: "Scheduled", gate: "24-Hour Shower Pan Flood Test & Radiant Subfloor Moisture Verification" },
  { code: "ST-27", num: 27, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "Frameless Starfire Tempered Glass Railings & Integrated Appliances", trade: "Glacier Architectural Glass & Appliance", csi: "10-28-00", preds: ["ST-26"], baseBudget: 44000, defaultStatus: "Scheduled", gate: "Structural P.Eng Base-Shoe Glass Guardrail Load Certification" },
  { code: "ST-28", num: 28, phase: 5, phaseLabel: "Phase V: Finishes & Millwork", name: "MEP Final Device Trims, Lutron Smart Lighting & HRV/Hydronic Balance", trade: "Howe Sound Elec & Sea-to-Sky Mech", csi: "26-51-00", preds: ["ST-27"], baseBudget: 39000, defaultStatus: "Scheduled", gate: "CRCA Air Balancing Report, Electrical Final Pass & Potable Water Flush" },

  // Phase VI: Civil Hardscaping, Final Blower Door, Schedules C-A/C-B & Occupancy (29-30)
  { code: "ST-29", num: 29, phase: 6, phaseLabel: "Phase VI: Hardscape & Occupancy", name: "Permeable Pavers, Exposed Aggregate Driveways & Native Alpine Planting", trade: "Tantalus Civil & Alpine Landscape", csi: "32-14-00", preds: ["ST-28"], baseBudget: 42000, defaultStatus: "Scheduled", gate: "Civil P.Eng Stormwater Permeable Retention & Municipal Boulevard Pass" },
  { code: "ST-30", num: 30, phase: 6, phaseLabel: "Phase VI: Hardscape & Occupancy", name: "Final Blower Door (<=1.0 ACH50), Schedules C-A/C-B & Occupancy Permit", trade: "Keystone Possibilities Ltd. (#52603) & City", csi: "01-77-00", preds: ["ST-29"], baseBudget: 18500, defaultStatus: "Scheduled", gate: "All 6 P.Eng Schedule C-B + Architect C-A + Municipal Occupancy Permit" }
];

const CANONICAL_6_PENG_DISCIPLINES = [
  {
    key: "GEOTECHNICAL",
    badge: "1. GEOTECHNICAL P.ENG",
    title: "Geotechnical Engineering, Bedrock Anchors, Shoring & Compaction",
    firm: "Thurber Geotechnical Engineering Ltd. — Dr. Arthur Tremblay, P.Eng.",
    permitEGBC: "EGBC Permit #1001948 • Schedule B & Field Memos #1–#4 Sealed",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-07, ST-10, ST-11",
    pdfName: "Geotechnical_Investigation_Bedrock_Shoring_Schedule_B.pdf",
    summary: "Borehole drilling & test-pit logs, competent granodiorite/basalt bedrock bearing verification (>300 kPa allowable), Hilti HIT-RE 500 epoxied 25M rock dowel anchorage, temporary excavation shoring piles, slope stability assessment, and 98% Standard Proctor Density (SPD) structural backfill compaction testing."
  },
  {
    key: "STRUCTURAL",
    badge: "2. STRUCTURAL P.ENG",
    title: "Structural Seismic Design, 35 MPa Concrete, Steel & #52603 Trusses",
    firm: "Apex Structural Engineering Ltd. — R. Vance, P.Eng., Struct.Eng.",
    permitEGBC: "EGBC Permit #1004821 • Schedule B Filed • IFC Rev 4 Sealed",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-09, ST-12, ST-13, ST-27",
    pdfName: "Structural_Seismic_Foundation_Framing_IFC_Rev4_Schedule_B.pdf",
    summary: "BCBC 2024 High-Seismic (Squamish/Whistler ground snow & PGA) structural calculations, 35 MPa concrete foundation walls, W12x65 steel moment frames, Simpson Strong-Tie ATS continuous tie-down rods, HDU8 shearwall hold-downs, Douglas Fir Glulam beams, and Dick's Lumber #52603 engineered roof truss package."
  },
  {
    key: "CIVIL",
    badge: "3. CIVIL & ES54 P.ENG",
    title: "Civil Site Servicing, 100-Yr Stormwater Detention & BC Hydro ES54",
    firm: "Tantalus Civil & Municipal Engineering — K. Mercer, P.Eng.",
    permitEGBC: "EGBC Permit #1003390 • Schedule B Filed • Sheet C-101 Sealed",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-08, ST-29",
    pdfName: "Civil_Stormwater_Detention_BCHydro_ES54_Schedule_B.pdf",
    summary: "On-site 100-year stormwater detention chamber & orifice flow control, 150mm SDR35 storm/sanitary municipal main connections, 50mm Type K copper domestic/fire watermain, ESC sediment & erosion control compliance, and BC Hydro ES54 underground primary duct bank & splice vault design."
  },
  {
    key: "MECHANICAL",
    badge: "4. MECHANICAL P.ENG",
    title: "Mechanical HVAC, Cold-Climate Heat Pumps, HRV & Hydronic Radiant",
    firm: "Sea-to-Sky Mechanical & Energy Engineering — L. Chen, P.Eng.",
    permitEGBC: "EGBC Permit #1005112 • Schedule B Filed • Sheet M-101 Sealed",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-04, ST-17, ST-18, ST-28",
    pdfName: "Mechanical_HVAC_HeatPump_StepCode4_Schedule_B.pdf",
    summary: "CSA F280-12 room-by-room heat loss/gain loads, Mitsubishi Variable-Capacity Cold-Climate Air-to-Water Heat Pumps (-25°C rated), Zehnder ComfoAir Q350 HRV (88% sensible recovery), multi-zone hydronic radiant floor loops, and BC Energy Step Code 4 / Zero Carbon EL-4 mechanical compliance."
  },
  {
    key: "ELECTRICAL",
    badge: "5. ELECTRICAL P.ENG",
    title: "Electrical 400A Primary Service, Multi-Unit Metering & EVEMS Load",
    firm: "Pacific Coast Electrical Engineering — D. Patel, P.Eng.",
    permitEGBC: "EGBC Permit #1006045 • Schedule B Filed • Sheet E-101 Sealed",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-08, ST-20, ST-28",
    pdfName: "Electrical_400A_EVEMS_SingleLine_Schedule_B.pdf",
    summary: "400A 120/240V underground primary service single-line diagram, multi-unit metering center, CEC Section 8 load calculation, intelligent EVEMS Level-2 EV charger load management, Lutron HomeWorks low-voltage lighting architecture, and hardwired interconnected smoke/CO life-safety network."
  },
  {
    key: "BUILDING_ENVELOPE",
    badge: "6. BUILDING ENVELOPE P.ENG",
    title: "Building Science Rainscreen Assembly, Thermal Modeling & NFPA 13D",
    firm: "Westcoast Building Science & Envelope P.Eng. — S. Lindqvist, P.Eng.",
    permitEGBC: "EGBC Permit #1002874 • Schedule B Filed • 2-5-10 Verified",
    status: "Sealed & Active ✓",
    stagesCovered: "ST-03, ST-10, ST-14, ST-15, ST-16, ST-19, ST-23",
    pdfName: "Building_Envelope_Rainscreen_AirBarrier_NFPA13D_Schedule_B.pdf",
    summary: "SIGA Majvest 200 continuous breathable air/weather barrier assembly, 60mm Rockwool Comfortboard 80 exterior insulation, 19mm ventilated capillary-break rainscreen cavity, NAFS triple-glazed window sill-pan flashing details, <=1.0 ACH50 blower door air-tightness protocol, and NFPA 13D/13R sprinkler integration."
  }
];

const CANONICAL_4_LOA_SCHEDULES = [
  {
    key: "SCHEDULE_A",
    code: "Schedule A",
    title: "Confirmation of Commitment by Owner & Coordinating Registered Professional (CRP)",
    status: "Filed & Stamped with Permit ✓",
    authority: "Wayne Stevenson (#52603) • Property Owner • Marcus Vance, Architect AIBC",
    stageGate: "Filed at Stage 05 (Building Permit Issuance)",
    pdfName: "BCBC2024_Schedule_A_Owner_And_CRP_Commitment.pdf",
    desc: "Statutory BC Building Code 2024 Schedule A signed by Property Owner and Coordinating Registered Professional (Marcus Vance, Architect AIBC) confirming full coordination of design and field reviews across all 6 P.Eng disciplines."
  },
  {
    key: "SCHEDULE_B",
    code: "Schedule B",
    title: "Assurance of Professional Design & Commitment for Field Review (All 6 P.Eng Disciplines)",
    status: "6 / 6 Disciplines Sealed & Filed ✓",
    authority: "Geotech • Structural • Civil ES54 • Mechanical • Electrical • Building Envelope P.Eng.",
    stageGate: "Filed at Stage 03 & Stage 05 (Active Field Reviews in Progress)",
    pdfName: "BCBC2024_Schedule_B_All_6_Engineering_Disciplines_Sealed.pdf",
    desc: "Complete statutory BC Building Code 2024 Schedule B Letters of Assurance signed and P.Eng.-sealed by Registered Professionals of Record for Geotechnical, Structural, Civil, Mechanical, Electrical, and Building Envelope."
  },
  {
    key: "SCHEDULE_CA",
    code: "Schedule C-A",
    title: "Assurance of Coordination of Professional Field Review (Pre-Occupancy CRP Sign-Off)",
    status: "Staged for Stage 30 Occupancy",
    authority: "Marcus Vance, Architect AIBC (Coordinating Registered Professional)",
    stageGate: "Required at Stage 30 prior to Municipal Occupancy Permit",
    pdfName: "BCBC2024_Schedule_CA_CRP_Final_Coordination_Template.pdf",
    desc: "Statutory BC Building Code 2024 Schedule C-A to be executed upon completion of Stage 30 confirming all 6 P.Eng Schedule C-B letters have been coordinated and the building substantially complies with the BCBC and Permit #BP2026-0419."
  },
  {
    key: "SCHEDULE_CB",
    code: "Schedule C-B",
    title: "Assurance of Professional Field Review & Compliance (6-Discipline Final Sign-Off)",
    status: "Geotech & Foundation Memos In • Final at Stage 30",
    authority: "All 6 Registered P.Eng. Disciplines (Geotech, Struct, Civil, Mech, Elec, Envelope)",
    stageGate: "Interim Memos Completed (Stages 07–12) • Final C-B at Stage 30",
    pdfName: "BCBC2024_Schedule_CB_Engineering_Compliance_Package.pdf",
    desc: "Statutory BC Building Code 2024 Schedule C-B assurance confirming completed field reviews and code compliance across Geotechnical, Structural, Civil, Mechanical, Electrical, and Building Envelope."
  }
];

const CANONICAL_7_SHEET_PLAN_DIFFS = [
  {
    sheet: "A-101",
    discipline: "ARCHITECTURAL",
    title: "Site Plan, Bill 44 Setbacks & Permeable Hardscape Coverage",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "Standard asphalt driveway apron; 1.5m North side-yard setback; 42.0% impermeable site coverage.",
    ifc_spec: "Upgraded to permeable interlocking eco-pavers (+8.5% stormwater infiltration credit); confirmed BCLS geodetic monument pins & tree protection zone.",
    delta_summary: "Added permeable paver retention system per Civil C-101 & verified BCLS pins.",
    impact_badge: "Stormwater Credit",
    sealed_by: "Marcus Vance, Architect AIBC"
  },
  {
    sheet: "A-201",
    discipline: "ARCHITECTURAL",
    title: "Level 1 & Level 2 Multiplex Floor Plans & STC 55+ Party Walls",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "Single 2x6 party wall with resilient channel (STC 52 nominal); 8'-0\" sliding patio door rough opening.",
    ifc_spec: "Upgraded to double-stud decoupled 2x4 acoustic party wall with dual Roxul Safe'n'Sound + double 5/8\" Type X drywall (STC 58+ verified); 10'-0\" EuroLine lift-slide rough opening.",
    delta_summary: "Upgraded party wall to STC 58+ double-stud assembly & widened glazing opening.",
    impact_badge: "Acoustic & Glazing Upgrade",
    sealed_by: "Marcus Vance, Architect AIBC"
  },
  {
    sheet: "S-101",
    discipline: "STRUCTURAL / GEOTECH",
    title: "35 MPa Concrete Foundation Plan, Stepped Bedrock Footings & Rock Dowels",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "28 MPa strip footings assumed on 150 kPa glacial till; standard 15M corner bars @ 16\" O.C.",
    ifc_spec: "35 MPa sulfate-resistant concrete stepped onto competent granodiorite bedrock (>300 kPa per Thurber Geotech G-101) with 26x 25M Hilti HIT-RE 500 epoxied rock dowels.",
    delta_summary: "Anchored 35 MPa stepped footings directly to bedrock per Thurber Geotech Schedule B.",
    impact_badge: "Structural & Geotech Upgrade",
    sealed_by: "Apex Structural P.Eng. & Thurber Geotech P.Eng."
  },
  {
    sheet: "S-202",
    discipline: "STRUCTURAL",
    title: "Level 2 Framing, Simpson ATS Continuous Tie-Downs & #52603 Roof Trusses",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "Standard discrete HDU5 hold-downs and 2x10 dimensional floor joists @ 16\" O.C.",
    ifc_spec: "Simpson Strong-Tie ATS continuous rod tie-down system (Grids A–D), 11-7/8\" Weyerhaeuser TJI 360 joists, Glulam ridge beams, and Dick's Lumber #52603 42 psf snow-load trusses.",
    delta_summary: "Upgraded to Simpson ATS continuous seismic rods & Dick's Lumber #52603 truss spec.",
    impact_badge: "Seismic & Truss Spec",
    sealed_by: "Apex Structural Engineering P.Eng."
  },
  {
    sheet: "C-101",
    discipline: "CIVIL / ES54",
    title: "Stormwater Detention Vault, Sanitary/Watermain & BC Hydro ES54 Duct Bank",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "Rock-pit soakaway trench and overhead temporary hydro service mast.",
    ifc_spec: "Engineered 100-year precast stormwater detention chamber with orifice control + permanent 4x 3\" DB2 underground BC Hydro ES54 duct bank and precast splice vault.",
    delta_summary: "Full underground BC Hydro ES54 duct bank & 100-yr detention tank approved by District.",
    impact_badge: "Civil ES54 Approved",
    sealed_by: "Tantalus Civil Engineering P.Eng."
  },
  {
    sheet: "M-101",
    discipline: "MECHANICAL",
    title: "Cold-Climate Air-to-Water Heat Pumps, Zehnder HRV & Step Code 4 Hydronics",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "Standard multi-split air-source heat pump + 70% SRE HRV.",
    ifc_spec: "Mitsubishi Variable-Capacity Cold-Climate Air-to-Water Heat Pump + Zehnder ComfoAir Q350 HRV (88% SRE) + multi-zone PEX-a radiant slab/subfloor manifolds (Step Code 4 / EL-4).",
    delta_summary: "Upgraded to 88% SRE Zehnder HRV & hydronic radiant zones for Step Code 4.",
    impact_badge: "Step Code 4 / EL-4",
    sealed_by: "Sea-to-Sky Mechanical P.Eng."
  },
  {
    sheet: "E-101",
    discipline: "ELECTRICAL",
    title: "400A Underground Primary Service, Multi-Metering & EVEMS Level-2 Chargers",
    permit_rev: "Rev 2 (Permit)",
    ifc_rev: "Rev 4 (Sealed IFC)",
    permit_spec: "200A main service with 1x 40A EV rough-in.",
    ifc_spec: "400A 120/240V underground primary service, 6-gang modular meter center, and 4x 48A Level-2 EVEMS load-managed charging stations.",
    delta_summary: "Upgraded to 400A primary service & 4-port EVEMS intelligent load management.",
    impact_badge: "400A + EVEMS",
    sealed_by: "Pacific Coast Electrical P.Eng."
  }
];

let currentTab7PhaseFilter = 0; // 0 = All 30 stages
let currentTab7DiffSheetFilter = "ALL";
let currentTab7DiffData = null;

function ensureJob30StagesState(job) {
  if (!job) return;
  if (!job.stage30Overrides || typeof job.stage30Overrides !== "object") {
    job.stage30Overrides = {};
  }
  // If job is KP-2026-002 (Chartwell - earlier stage) or KP-2026-003 (Whistler - further along), seed realistic stage progress if empty
  if (Object.keys(job.stage30Overrides).length === 0) {
    let completedUpTo = 12;
    let activeNum = 13;
    if (job.jobId === "KP-2026-002") {
      completedUpTo = 8;
      activeNum = 9;
    } else if (job.jobId === "KP-2026-003") {
      completedUpTo = 14;
      activeNum = 15;
    }
    CANONICAL_30_STAGES_MASTER.forEach(st => {
      if (st.num <= completedUpTo) {
        job.stage30Overrides[st.code] = "Completed";
      } else if (st.num === activeNum) {
        job.stage30Overrides[st.code] = "Active On-Site";
      } else {
        job.stage30Overrides[st.code] = "Scheduled";
      }
    });
  }
}

function getComputed30StagesForJob(job) {
  ensureJob30StagesState(job);
  const scale = Number(job.contractPrice) ? (Number(job.contractPrice) / 1850000) : 1.0;
  return CANONICAL_30_STAGES_MASTER.map(st => {
    const status = job.stage30Overrides[st.code] || st.defaultStatus;
    const budget = Math.round(st.baseBudget * scale);
    const invoiced = status === "Completed" ? budget : (status === "Active On-Site" ? Math.round(budget * 0.5) : 0);
    const holdback10 = Math.round(invoiced * 0.10);
    const net90 = invoiced - holdback10;
    return Object.assign({}, st, {
      status,
      budget,
      invoiced,
      holdback10,
      net90
    });
  });
}

function renderTab7ThirtyStagesAndGeotech() {
  const job = getActiveJob();
  if (!job) return;
  const stages = getComputed30StagesForJob(job);

  const completedStages = stages.filter(s => s.status === "Completed");
  const activeStage = stages.find(s => s.status === "Active On-Site") || stages.find(s => s.status !== "Completed") || stages[stages.length - 1];

  // Calculate total invoiced & 10% holdback across Tab 6 / 30 stages
  let totalInvoiced = 0;
  try {
    const secs = collectHighland5SectionsData(job);
    secs.forEach(sec => {
      sec.items.forEach(it => {
        if (it.paid) totalInvoiced += (Number(it.amount) || 0);
      });
    });
  } catch (e) {}
  if (totalInvoiced <= 0) {
    totalInvoiced = stages.reduce((acc, s) => acc + s.invoiced, 0);
  }
  const totalHoldback10 = Math.round(totalInvoiced * 0.10);

  // Header & Top 4 KPI Cards
  const badgeEl = document.getElementById("p7-job-id-badge");
  if (badgeEl) badgeEl.innerText = job.jobId + " • BC BUILDER #52603";
  const titleEl = document.getElementById("p7-master-title");
  if (titleEl) titleEl.innerText = job.address + " — 30-Stage Construction, Geotech & 6-Discipline Engineering";

  const kpiProg = document.getElementById("p7-kpi-stages-progress");
  const kpiProgSub = document.getElementById("p7-kpi-stages-sub");
  if (kpiProg) kpiProg.innerText = `${completedStages.length} / 30 Completed`;
  if (kpiProgSub && activeStage) {
    kpiProgSub.innerText = `${activeStage.code} Active • ${activeStage.name}`;
  }

  const kpiHb = document.getElementById("p7-kpi-holdback-val");
  const kpiHbSub = document.getElementById("p7-kpi-holdback-sub");
  if (kpiHb) kpiHb.innerText = fmtMoney(totalHoldback10) + " Retained";
  if (kpiHbSub) kpiHbSub.innerText = `10.0% of ${fmtMoney(totalInvoiced)} Certified Draws (SBC 1997 c.45)`;

  // 1. Render 6-Discipline P.Eng & Geotechnical Grid
  const pengGrid = document.getElementById("p7-peng-disciplines-grid");
  if (pengGrid) {
    pengGrid.innerHTML = CANONICAL_6_PENG_DISCIPLINES.map(d => {
      const pdfFile = `${job.jobId}_${d.pdfName}`;
      return `
        <div
          onclick="openTab7PengDisciplinePdf('${escapeHtml(d.key)}')"
          style="background:#0b0f17; border:1px solid ${d.key === 'GEOTECHNICAL' ? '#d4af37' : 'rgba(212,175,55,0.34)'}; border-radius:12px; padding:13px 15px; cursor:pointer; display:flex; flex-direction:column; justify-content:space-between; gap:8px; transition:all 0.18s ease;"
          title="Click to open sealed ${escapeHtml(d.badge)} report & Schedule B PDF"
        >
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:6px;">
              <span class="kp-badge-pill kp-badge-gold">${escapeHtml(d.badge)}</span>
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(d.status)}</span>
            </div>
            <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.9rem; font-weight:900; color:#ffffff; line-height:1.3;">
              ${escapeHtml(d.title)}
            </div>
            <div style="font-size:0.74rem; font-weight:700; color:#d4af37; margin-top:4px;">
              ${escapeHtml(d.firm)}
            </div>
            <div style="font-size:0.69rem; color:#94a3b8; margin-top:2px;">
              ${escapeHtml(d.permitEGBC)} &bull; Stages: <strong style="color:#ffffff;">${escapeHtml(d.stagesCovered)}</strong>
            </div>
            <div style="font-size:0.73rem; color:#cbd5e1; margin-top:7px; line-height:1.45;">
              ${escapeHtml(d.summary)}
            </div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; padding-top:8px; border-top:1px solid rgba(255,255,255,0.08); margin-top:4px;">
            <span style="font-size:0.68rem; color:#f3e5ab; font-weight:700; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              📄 ${escapeHtml(pdfFile)}
            </span>
            <span class="kp-gold-btn kp-pill-sm" style="padding:3px 10px !important; font-size:0.68rem !important;">
              Open PDF &rarr;
            </span>
          </div>
        </div>
      `;
    }).join("");
  }

  // 2. Render BCBC 2024 Statutory Letters of Assurance Bar (Schedule A, B, C-A, C-B)
  const loaBar = document.getElementById("p7-loa-schedules-bar");
  if (loaBar) {
    const customLoas = (job.planSets && job.planSets.loa_schedules) ? job.planSets.loa_schedules : {};
    loaBar.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px; padding-bottom:7px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">BC BUILDING CODE 2024 LETTERS OF ASSURANCE</span>
          <span style="font-family:'Outfit','Plus Jakarta Sans',sans-serif; font-size:0.9rem; font-weight:900; color:#ffffff;">
            Statutory Schedules A, B, C-A &amp; C-B Compliance Vault (${escapeHtml(resolveJobMunicipality(job))} &bull; Permit #${escapeHtml(job.permitNum || 'BP2026-0419')})
          </span>
        </div>
        <span style="font-size:0.72rem; color:#cbd5e1;">Click any Schedule below to inspect or print the sealed statutory assurance</span>
      </div>
      <div style="display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:9px;">
        ${CANONICAL_4_LOA_SCHEDULES.map(sc => {
          const ov = customLoas[sc.key.toLowerCase()] || null;
          const stText = ov ? (ov.status + " (" + ov.signed_date + ")") : sc.status;
          const fnText = ov && ov.pdf_filename ? ov.pdf_filename : `${job.jobId}_${sc.pdfName}`;
          return `
            <div
              onclick="openTab7LoaSchedulePdf('${escapeHtml(sc.key)}')"
              style="background:#05070b; border:1px solid rgba(212,175,55,0.36); border-radius:10px; padding:10px 12px; cursor:pointer; display:flex; flex-direction:column; justify-content:space-between; gap:6px;"
              title="Click to open ${escapeHtml(sc.code)} PDF"
            >
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; gap:4px; flex-wrap:wrap;">
                  <span class="kp-badge-pill kp-badge-gold">${escapeHtml(sc.code)}</span>
                  <span style="font-size:0.65rem; font-weight:800; color:#f3e5ab;">${escapeHtml(stText)}</span>
                </div>
                <div style="font-size:0.78rem; font-weight:800; color:#ffffff; margin-top:5px; line-height:1.3;">
                  ${escapeHtml(sc.title)}
                </div>
                <div style="font-size:0.68rem; color:#94a3b8; margin-top:3px;">
                  ${escapeHtml(sc.authority)}
                </div>
              </div>
              <div style="font-size:0.66rem; color:#d4af37; font-weight:700; padding-top:5px; border-top:1px solid rgba(255,255,255,0.07); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                📄 ${escapeHtml(fnText)}
              </div>
            </div>
          `;
        }).join("")}
      </div>
    `;
  }

  // 3. Render Side-by-Side Blueprint Revision Diff Drawer
  renderPortalPlanRevisionDiff(currentTab7DiffSheetFilter);

  // 4. Update DAG Mobilization Banner
  const dagHeadline = document.getElementById("p7-dag-banner-headline");
  const dagSub = document.getElementById("p7-dag-banner-sub");
  if (dagHeadline && activeStage) {
    const nextStages = stages.filter(s => (s.preds || []).includes(activeStage.code));
    const nextLabel = nextStages.length > 0 ? nextStages.map(n => `${n.code} (${n.name.split(',')[0]})`).join(", ") : "ST-30 Final Occupancy";
    dagHeadline.innerHTML = `${escapeHtml(activeStage.code)} Active: <span style="color:#d4af37;">${escapeHtml(activeStage.name)}</span> &mdash; Next DAG Successor: <span style="color:#f3e5ab;">${escapeHtml(nextLabel)}</span>`;
  }
  if (dagSub) {
    dagSub.innerText = `${completedStages.length} of 30 canonical stages completed. Click any stage status button below to cycle status (Completed / Active On-Site / Scheduled) or click Auto-Notify Next Trade to dispatch mobilization.`;
  }

  // 5. Render 30-Stage Master Checklist
  const filteredStages = currentTab7PhaseFilter === 0
    ? stages
    : stages.filter(s => s.phase === currentTab7PhaseFilter);

  const countBadge = document.getElementById("p7-stages-filter-count-badge");
  if (countBadge) {
    countBadge.innerText = currentTab7PhaseFilter === 0
      ? `Showing All 30 Start-to-Finish Stages (${completedStages.length}/30 Completed)`
      : `Phase ${currentTab7PhaseFilter}: Showing ${filteredStages.length} Stages`;
  }

  document.querySelectorAll(".p7-phase-pill").forEach(btn => {
    const p = Number(btn.getAttribute("data-phase") || 0);
    if (p === currentTab7PhaseFilter) {
      btn.className = "kp-gold-btn kp-pill-sm p7-phase-pill";
    } else {
      btn.className = "kp-secondary-btn kp-pill-sm p7-phase-pill";
    }
  });

  const listEl = document.getElementById("p7-thirty-stages-list");
  if (listEl) {
    listEl.innerHTML = filteredStages.map(st => {
      const isDone = st.status === "Completed";
      const isActive = st.status === "Active On-Site";
      const borderCol = isActive ? "#d4af37" : (isDone ? "rgba(212,175,55,0.38)" : "rgba(255,255,255,0.14)");
      const bgCol = isActive ? "linear-gradient(90deg, rgba(212,175,55,0.12) 0%, #070a10 100%)" : "#070a10";
      const predsText = st.preds && st.preds.length > 0 ? st.preds.join(", ") : "None (Project Start)";

      return `
        <div
          style="background:${bgCol}; border:1px solid ${borderCol}; border-radius:11px; padding:10px 14px; display:grid; grid-template-columns:minmax(0, 2.2fr) minmax(0, 1.3fr) auto; align-items:center; gap:12px;"
        >
          <!-- Left: Stage Code, Name, Trade, CSI & Predecessor Gate -->
          <div style="min-width:0;">
            <div style="display:flex; align-items:center; gap:7px; flex-wrap:wrap; margin-bottom:4px;">
              <span class="kp-badge-pill kp-badge-gold">${escapeHtml(st.code)}</span>
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(st.phaseLabel)}</span>
              <span style="font-size:0.68rem; color:#94a3b8; font-weight:700;">CSI ${escapeHtml(st.csi)} &bull; Preds: <strong style="color:#ffffff;">${escapeHtml(predsText)}</strong></span>
            </div>
            <div style="font-size:0.88rem; font-weight:900; color:#ffffff; line-height:1.3;">
              ${escapeHtml(st.name)}
            </div>
            <div style="font-size:0.73rem; color:#cbd5e1; margin-top:3px;">
              Trade / Authority: <strong style="color:#f3e5ab;">${escapeHtml(st.trade)}</strong> &bull; QA Gate: <span style="color:#94a3b8;">${escapeHtml(st.gate)}</span>
            </div>
          </div>

          <!-- Middle: Budget, Invoiced, 10% Lien Holdback & 90% Net -->
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; background:#05070b; border:1px solid rgba(255,255,255,0.1); border-radius:9px; padding:7px 10px; font-size:0.72rem;">
            <div>
              <div style="font-size:0.62rem; color:#94a3b8; text-transform:uppercase; font-weight:800;">Stage Budget</div>
              <div style="font-size:0.82rem; font-weight:900; color:#ffffff; margin-top:1px;">${fmtMoney(st.budget)}</div>
            </div>
            <div>
              <div style="font-size:0.62rem; color:#f3e5ab; text-transform:uppercase; font-weight:800;">10% Holdback</div>
              <div style="font-size:0.82rem; font-weight:900; color:#d4af37; margin-top:1px;">${fmtMoney(st.holdback10)}</div>
            </div>
            <div>
              <div style="font-size:0.62rem; color:#94a3b8; text-transform:uppercase; font-weight:800;">90% Net Paid</div>
              <div style="font-size:0.82rem; font-weight:900; color:#ffffff; margin-top:1px;">${fmtMoney(st.net90)}</div>
            </div>
          </div>

          <!-- Right: Interactive Status Pill + Spec PDF + Notify Next Trade -->
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; justify-content:flex-end;">
            <button
              type="button"
              onclick="toggleTab7StageStatus('${escapeHtml(st.code)}')"
              class="${isDone || isActive ? 'kp-gold-btn' : 'kp-secondary-btn'} kp-pill-sm"
              style="min-width:130px; justify-content:center;"
              title="Click to cycle stage status (Completed / Active On-Site / Scheduled)"
            >
              ${isDone ? "✓ COMPLETED" : (isActive ? "⚡ ACTIVE ON-SITE" : "⏳ SCHEDULED")}
            </button>
            <button
              type="button"
              onclick="openTab7StageSpecPdf('${escapeHtml(st.code)}')"
              class="kp-secondary-btn kp-pill-sm"
              title="Open Stage Specification, Geotech/Eng Gate & Holdback PDF"
            >
              📄 Spec PDF
            </button>
            <button
              type="button"
              onclick="triggerPortalNextTradeNotification('${escapeHtml(st.code)}')"
              class="kp-secondary-btn kp-pill-sm"
              title="Dispatch DAG Next-Trade Mobilization Notice from ${escapeHtml(st.code)}"
            >
              📨 Notify Next
            </button>
          </div>
        </div>
      `;
    }).join("");
  }
}

function filterTab7StagesByPhase(phaseNum) {
  currentTab7PhaseFilter = Number(phaseNum) || 0;
  renderTab7ThirtyStagesAndGeotech();
}

function toggleTab7StageStatus(stageCode) {
  const job = getActiveJob();
  if (!job) return;
  ensureJob30StagesState(job);
  const cur = job.stage30Overrides[stageCode] || "Scheduled";
  const order = ["Scheduled", "Active On-Site", "Completed"];
  const next = order[(order.indexOf(cur) + 1) % order.length];
  job.stage30Overrides[stageCode] = next;
  saveState();
  renderTab7ThirtyStagesAndGeotech();
  showToast(`Updated ${stageCode} status to: ${next}`);
}

function openTab7StageSpecPdf(stageCode) {
  const job = getActiveJob();
  const stages = getComputed30StagesForJob(job);
  const st = stages.find(s => s.code === stageCode);
  if (!st) return;

  const pdfName = `${job.jobId}_${st.code}_Scope_Gate_And_Holdback.pdf`;
  const lines = [
    `KEYSTONE POSSIBILITIES LTD. (BC LICENSED BUILDER #52603) — 30-STAGE EXECUTION RECORD`,
    `PROJECT: ${job.address} (${job.jobId}) | PERMIT #${job.permitNum || 'BP2026-0419'}`,
    `STAGE: ${st.code} — ${st.name} (${st.phaseLabel})`,
    `CSI MASTERFORMAT: ${st.csi} | PREDECESSOR STAGES: ${(st.preds && st.preds.length) ? st.preds.join(', ') : 'None'}`,
    `ASSIGNED TRADE / AUTHORITY: ${st.trade}`,
    `CURRENT STATUS: ${st.status.toUpperCase()}`,
    `------------------------------------------------------------------------`,
    `FINANCIAL & STATUTORY 10% BUILDERS LIEN HOLDBACK BREAKDOWN:`,
    `  • Stage Scheduled Budget:        ${fmtMoney(st.budget)}`,
    `  • Certified Invoiced to Date:    ${fmtMoney(st.invoiced)}`,
    `  • 10% Statutory Lien Holdback:   ${fmtMoney(st.holdback10)} (Retained in SBC 1997 c.45 Trust)`,
    `  • 90% Net Payable Disbursed:     ${fmtMoney(st.net90)}`,
    `------------------------------------------------------------------------`,
    `MANDATORY QA, GEOTECHNICAL & P.ENG INSPECTION GATE:`,
    `  ${st.gate}`,
    `------------------------------------------------------------------------`,
    `CERTIFIED BY: Wayne Stevenson — BC Housing Licensed Builder #52603`
  ];

  openCustomVaultPdfOnScreen(
    `${st.code}: ${st.name}`,
    pdfName,
    `${st.phaseLabel} • CSI ${st.csi} • Status: ${st.status} • 10% Holdback: ${fmtMoney(st.holdback10)}`,
    lines.join("\n"),
    ""
  );
}

function openTab7PengDisciplinePdf(discKey) {
  const job = getActiveJob();
  const d = CANONICAL_6_PENG_DISCIPLINES.find(x => x.key === discKey) || CANONICAL_6_PENG_DISCIPLINES[0];
  const pdfName = `${job.jobId}_${d.pdfName}`;
  const lines = [
    `KEYSTONE POSSIBILITIES LTD. (#52603) — 6-DISCIPLINE ENGINEERING & GEOTECHNICAL VAULT`,
    `PROJECT: ${job.address} (${job.jobId}) | MUNICIPALITY: ${resolveJobMunicipality(job)}`,
    `DISCIPLINE: ${d.badge} — ${d.title}`,
    `ENGINEER OF RECORD: ${d.firm}`,
    `EGBC & ASSURANCE STATUS: ${d.permitEGBC} (${d.status})`,
    `STAGES GOVERNED: ${d.stagesCovered}`,
    `------------------------------------------------------------------------`,
    `TECHNICAL SCOPE & FIELD REVIEW CERTIFICATION:`,
    d.summary,
    `------------------------------------------------------------------------`,
    `BC BUILDING CODE 2024 SCHEDULE B & C-B FIELD REVIEW LOG:`,
    `  • Schedule B Assurance of Professional Design & Commitment for Field Review: FILED & SEALED`,
    `  • Competent Subgrade / Structural / Service Field Memos: VERIFIED ON SITE`,
    `  • Coordinated by: Marcus Vance, Architect AIBC & Wayne Stevenson (BC Builder #52603)`
  ];
  openCustomVaultPdfOnScreen(
    `${d.badge} — ${d.title}`,
    pdfName,
    `${d.firm} • ${d.permitEGBC}`,
    lines.join("\n"),
    ""
  );
}

function openTab7LoaSchedulePdf(schedKey) {
  const job = getActiveJob();
  const sc = CANONICAL_4_LOA_SCHEDULES.find(x => x.key === schedKey) || CANONICAL_4_LOA_SCHEDULES[0];
  const pdfName = `${job.jobId}_${sc.pdfName}`;
  const lines = [
    `BRITISH COLUMBIA BUILDING CODE 2024 — STATUTORY LETTER OF ASSURANCE`,
    `SCHEDULE: ${sc.code} — ${sc.title}`,
    `PROJECT ADDRESS: ${job.address} (${job.jobId}) | BUILDING PERMIT #${job.permitNum || 'BP2026-0419'}`,
    `MUNICIPAL JURISDICTION: ${resolveJobMunicipality(job)}`,
    `REGISTERED AUTHORITY: ${sc.authority}`,
    `FILING STATUS: ${sc.status} (${sc.stageGate})`,
    `------------------------------------------------------------------------`,
    sc.desc,
    `------------------------------------------------------------------------`,
    `6-DISCIPLINE P.ENG COORDINATION MATRIX:`,
    `  1. Geotechnical P.Eng:      Thurber Geotechnical Engineering Ltd. (Dr. Arthur Tremblay, P.Eng.)`,
    `  2. Structural P.Eng:        Apex Structural Engineering Ltd. (EGBC #1004821)`,
    `  3. Civil & ES54 P.Eng:      Tantalus Civil & Municipal Engineering P.Eng.`,
    `  4. Mechanical HVAC P.Eng:   Sea-to-Sky Mechanical & Energy Engineering P.Eng.`,
    `  5. Electrical 400A P.Eng:   Pacific Coast Electrical Engineering P.Eng.`,
    `  6. Building Envelope P.Eng: Westcoast Building Science & Envelope P.Eng.`,
    `------------------------------------------------------------------------`,
    `LICENSED BUILDER: Wayne Stevenson — Keystone Possibilities Ltd. (BC Housing #52603)`
  ];
  openCustomVaultPdfOnScreen(
    `BCBC 2024 ${sc.code} — ${sc.title}`,
    pdfName,
    `${sc.status} • ${sc.authority}`,
    lines.join("\n"),
    ""
  );
}

function openGeotechAndLoaSummaryPdf() {
  openTab7PengDisciplinePdf("GEOTECHNICAL");
}

function renderPortalPlanRevisionDiff(sheetFilter) {
  currentTab7DiffSheetFilter = sheetFilter || currentTab7DiffSheetFilter || "ALL";
  const drawer = document.getElementById("p7-plan-revision-diff-drawer");
  if (!drawer) return;

  const job = getActiveJob();
  const sourceDeltas = (currentTab7DiffData && Array.isArray(currentTab7DiffData.deltas) && currentTab7DiffData.deltas.length > 0)
    ? currentTab7DiffData.deltas
    : CANONICAL_7_SHEET_PLAN_DIFFS;

  const filtered = currentTab7DiffSheetFilter === "ALL"
    ? sourceDeltas
    : sourceDeltas.filter(d => d.sheet === currentTab7DiffSheetFilter);

  const sheetButtons = ["ALL", "A-101", "A-201", "S-101", "S-202", "C-101", "M-101", "E-101"].map(code => {
    const active = currentTab7DiffSheetFilter === code;
    return `<button type="button" onclick="renderPortalPlanRevisionDiff('${code}')" class="${active ? 'kp-gold-btn' : 'kp-secondary-btn'} kp-pill-sm" style="padding:3px 10px !important; font-size:0.68rem !important;">${code === 'ALL' ? 'All 7 Sheets' : code}</button>`;
  }).join("");

  drawer.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.1);">
      <div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="kp-badge-pill kp-badge-gold">BLUEPRINT REVISION DIFF ENGINE</span>
          <span class="kp-badge-pill kp-badge-white">Permit Set (Rev 2) vs Sealed IFC Set (Rev 4)</span>
        </div>
        <div style="font-size:0.78rem; color:#cbd5e1; margin-top:4px;">
          Side-by-side comparison across Architectural, Geotechnical, Structural, Civil ES54, Mechanical &amp; Electrical sheets for <strong style="color:#ffffff;">${escapeHtml(job ? job.address : '')}</strong>
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:5px; flex-wrap:wrap;">
        ${sheetButtons}
      </div>
    </div>

    <div style="display:flex; flex-direction:column; gap:8px;">
      ${filtered.map(item => `
        <div style="background:#0b0f17; border:1px solid rgba(212,175,55,0.32); border-radius:10px; padding:10px 13px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:7px;">
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-gold">${escapeHtml(item.sheet)} &bull; ${escapeHtml(item.discipline)}</span>
              <span style="font-size:0.84rem; font-weight:900; color:#ffffff;">${escapeHtml(item.title)}</span>
            </div>
            <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(item.impact_badge)}</span>
              <span style="font-size:0.7rem; color:#d4af37; font-weight:700;">Sealed: ${escapeHtml(item.sealed_by)}</span>
            </div>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; font-size:0.74rem;">
            <div style="background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:8px; padding:8px 10px;">
              <div style="font-size:0.65rem; font-weight:800; color:#94a3b8; text-transform:uppercase; margin-bottom:3px;">
                ${escapeHtml(item.permit_rev)} — Baseline Municipal Permit Spec
              </div>
              <div style="color:#cbd5e1; line-height:1.45;">${escapeHtml(item.permit_spec)}</div>
            </div>
            <div style="background:#05070b; border:1px solid rgba(212,175,55,0.45); border-radius:8px; padding:8px 10px;">
              <div style="font-size:0.65rem; font-weight:800; color:#f3e5ab; text-transform:uppercase; margin-bottom:3px;">
                ${escapeHtml(item.ifc_rev)} — Upgraded Sealed IFC Spec ✓
              </div>
              <div style="color:#ffffff; line-height:1.45;">${escapeHtml(item.ifc_spec)}</div>
            </div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

async function togglePortalPlanRevisionDiff(sheetFilter) {
  const drawer = document.getElementById("p7-plan-revision-diff-drawer");
  const job = getActiveJob();
  if (drawer && !sheetFilter) {
    drawer.style.display = "block";
  }
  renderPortalPlanRevisionDiff(sheetFilter || "ALL");
  showToast("🔍 Loaded Side-by-Side Blueprint Revision Diff (Permit Rev 2 vs Sealed IFC Rev 4)");
}

async function triggerPortalNextTradeNotification(explicitStageCode) {
  const job = getActiveJob();
  const stages = getComputed30StagesForJob(job);
  let triggerCode = explicitStageCode;
  if (!triggerCode) {
    const completed = stages.filter(s => s.status === "Completed");
    triggerCode = completed.length > 0 ? completed[completed.length - 1].code : "ST-12";
  }

  let serverData = null;

  const curStage = stages.find(s => s.code === triggerCode) || stages[11];
  const unlocked = stages.filter(s => (s.preds || []).includes(triggerCode));
  const primaryNext = (serverData && serverData.primary_next_stage)
    ? serverData.primary_next_stage
    : (unlocked[0] || stages[Math.min(stages.length - 1, curStage.num)]);

  const subj = (serverData && serverData.mobilization_subject)
    ? serverData.mobilization_subject
    : `[KEYSTONE #52603 MOBILIZATION] ${job.jobId} (${job.address}) — ${primaryNext.code}: ${primaryNext.name}`;

  const bodyText = (serverData && serverData.mobilization_body)
    ? serverData.mobilization_body
    : [
        `OFFICIAL DAG NEXT-TRADE MOBILIZATION DIRECTIVE`,
        `PROJECT: ${job.address} (${job.jobId}) | PERMIT #${job.permitNum || 'BP2026-0419'}`,
        `COMPLETED PREDECESSOR STAGE: ${triggerCode} (${curStage.name}) — VERIFIED COMPLETE ✓`,
        `UNLOCKED SUCCESSOR STAGE: ${primaryNext.code} — ${primaryNext.name}`,
        `DISPATCHED TO TRADE: ${primaryNext.trade || 'Assigned Subcontractor'}`,
        `------------------------------------------------------------------------`,
        `Please mobilize crew and materials to ${job.address} per the Keystone Possibilities Ltd. (#52603) 30-Stage Master Schedule.`,
        `All predecessor engineering and municipal inspection gates (${curStage.gate}) have been signed off.`,
        `------------------------------------------------------------------------`,
        `Issued by: Wayne Stevenson — President, Keystone Possibilities Ltd. (BC Housing Builder #52603)`
      ].join("\n");

  openCustomVaultPdfOnScreen(
    `DAG Trade Mobilization Dispatched — ${primaryNext.code}`,
    `${job.jobId}_Mobilization_Notice_${primaryNext.code}.pdf`,
    `Trigger: ${triggerCode} Complete ✓ → Unlocked: ${unlocked.map(u => u.code).join(', ') || primaryNext.code}`,
    subj + "\n\n" + bodyText,
    ""
  );
  showToast(`📨 Dispatched Next-Trade Mobilization Notice for ${primaryNext.code} (${primaryNext.name})`);
}

async function exportPortalBankDrawHoldbackPdf() {
  const job = getActiveJob();
  const sections = collectHighland5SectionsData(job);
  const revStats = getJobSignedRevisionsSum(job);
  const revisedContract = (Number(job.contractPrice) || 0) + revStats.signedSum;

  let grossPaid = 0;
  let grossTotal = 0;
  let paidCount = 0;
  sections.forEach(sec => {
    sec.items.forEach(it => {
      const a = Number(it.amount) || 0;
      grossTotal += a;
      if (it.paid) {
        grossPaid += a;
        paidCount++;
      }
    });
  });

  const certifiedGross = grossPaid > 0 ? grossPaid : grossTotal;
  const holdback10 = Math.round(certifiedGross * 0.10);
  const netPayable90 = certifiedGross - holdback10;
  const cmFee125 = Math.round(certifiedGross * 0.125);

  let daemonResult = null;

  const pdfFilename = (daemonResult && daemonResult.filename)
    ? daemonResult.filename
    : `${job.jobId}_Bank_Draw_Lien_Certificate.pdf`;

  const certLines = [
    `CCDC 5B PROGRESS DRAW & 10% STATUTORY BUILDERS LIEN HOLDBACK CERTIFICATE`,
    `BUILDER: Keystone Possibilities Ltd. — Wayne Stevenson (BC Housing Licensed Builder #52603)`,
    `PROJECT: ${job.address} (${job.jobId}) | MUNICIPALITY: ${resolveJobMunicipality(job)}`,
    `BUILDING PERMIT: #${job.permitNum || 'BP2026-0419'} | PID: ${job.pid || '014-882-192'}`,
    `PROPERTY OWNER(S): ${job.ownerName}`,
    `STATUTORY AUTHORITY: British Columbia Builders Lien Act (SBC 1997, c. 45, Section 5)`,
    `========================================================================`,
    `1. REVISED PRIME CONTRACT VALUE:              ${fmtMoney(revisedContract)}`,
    `2. GROSS CERTIFIED INVOICED TO DATE (100%):   ${fmtMoney(certifiedGross)} (${paidCount} Verified Draws)`,
    `3. LESS 10.0% STATUTORY LIEN HOLDBACK TRUST:  -${fmtMoney(holdback10)} (Retained in Escrow)`,
    `4. NET 90.0% PAYABLE DISBURSED TO TRADES:     ${fmtMoney(netPayable90)}`,
    `5. CCDC 5B BUILDER CM FEE (12.5%):            ${fmtMoney(cmFee125)}`,
    `========================================================================`,
    `MATHEMATICAL & STATUTORY INVARIANT VERIFICATION:`,
    `  10% Holdback (${fmtMoney(holdback10)}) + 90% Net Payable (${fmtMoney(netPayable90)}) = 100% Gross (${fmtMoney(certifiedGross)}) ✓`,
    `  55-Day Builders Lien Holdback Release Period Governed by SBC 1997 c. 45.`,
    `  Saved to Job Vault: ${daemonResult && daemonResult.pdf_path ? daemonResult.pdf_path : ('01_contracts/' + pdfFilename)}`,
    `------------------------------------------------------------------------`,
    `CERTIFIED BY: Wayne Stevenson — BC Housing Licensed Builder #52603`
  ];

  openCustomVaultPdfOnScreen(
    `CCDC 5B Bank Draw & 10% Lien Holdback Certificate — ${job.jobId}`,
    pdfFilename,
    `Gross Certified: ${fmtMoney(certifiedGross)} • 10% Holdback Trust: ${fmtMoney(holdback10)} • 90% Net Payable: ${fmtMoney(netPayable90)}`,
    certLines.join("\n"),
    ""
  );
  triggerDummyDownload(pdfFilename, certLines.join("\n"));
  showToast(`📄 Exported 10% Lien Holdback & Bank Draw Certificate: ${pdfFilename}`);
}

async function syncPortalFromDaemonV10Jobs(silent) {
  await hydrateFromWordPressServer();
  const pill = document.getElementById("p7-live-hub-sync-pill");
  if (pill) {
    const ts = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    pill.innerText = "✓ Cloud Vault Synced (" + ts + ")";
  }
  if (!silent) {
    renderAllPortalComponents();
    showToast("Synced project plans, geotech & ledger with Keystone Cloud Vault");
  }
}

// Auto-select job or tab from URL query params (?job=KP-2026-001&tab=7)
function applyUrlQueryParamsOnLoad() {
  try {
    const params = new URLSearchParams(window.location.search || "");
    const qJob = params.get("job") || params.get("job_id");
    if (qJob && portalStore && Array.isArray(portalStore.jobs)) {
      const found = portalStore.jobs.find(j => j.jobId.toUpperCase() === qJob.trim().toUpperCase());
      if (found) {
        portalStore.activeJobId = found.jobId;
        renderJobSelectors();
      }
    }
    const qTab = Number(params.get("tab") || 0);
    if (qTab >= 1 && qTab <= 6) {
      launchDemoProject();
      switchPortalPage(qTab);
    }
  } catch (e) {}
}

window.renderTab7ThirtyStagesAndGeotech = renderTab7ThirtyStagesAndGeotech;
window.filterTab7StagesByPhase = filterTab7StagesByPhase;
window.toggleTab7StageStatus = toggleTab7StageStatus;
window.openTab7StageSpecPdf = openTab7StageSpecPdf;
window.openTab7PengDisciplinePdf = openTab7PengDisciplinePdf;
window.openTab7LoaSchedulePdf = openTab7LoaSchedulePdf;
window.openGeotechAndLoaSummaryPdf = openGeotechAndLoaSummaryPdf;
window.renderPortalPlanRevisionDiff = renderPortalPlanRevisionDiff;
window.togglePortalPlanRevisionDiff = togglePortalPlanRevisionDiff;
window.triggerPortalNextTradeNotification = triggerPortalNextTradeNotification;
window.exportPortalBankDrawHoldbackPdf = exportPortalBankDrawHoldbackPdf;
window.syncPortalFromDaemonV10Jobs = syncPortalFromDaemonV10Jobs;

setTimeout(() => {
  try {
    applyUrlQueryParamsOnLoad();
    renderTab7ThirtyStagesAndGeotech();
    syncPortalFromDaemonV10Jobs(true);
  } catch (e) {}
}, 180);

setInterval(() => {
  if (document.visibilityState === "visible") {
    syncPortalFromDaemonV10Jobs(true);
  }
}, 10000);











// ============================================================================
// KEYSTONE PORTAL v11.0 EXECUTIVE SIMPLIFICATION (v13.0 3-BOX ARCHITECTURE:
//   BOX 1: CONSULTANTS (Architect, Structural Eng, Geotech, BCLS Survey, Step Code, Envelope)
//   BOX 2: TRADES (Name, Person We're Working With, Signed Contract)
//   BOX 3: CITY INSPECTIONS, PERMITS & SCHEDULES (Schedule A, Schedule B, C-A, C-B)
//          -> Clicking Box 3 opens the Master Page with 3 Master Brackets:
//             1. Master Plans & Schedules (Schedule A / B / C-A / C-B)
//             2. Permits Made / Pulled
//             3. All Inspection Reports Underneath)
// ============================================================================

let selectedP4ViewMode = "list"; // "list" | "partner" | "city_master"

function getCleanPropertyTypeLabel(job) {
  if (!job) return "Custom Residence";
  const raw = String(job.title || job.projectType || "").trim();
  const addr = String(job.address || "").toLowerCase();
  if (/multiplex|4-unit|4 unit|bill 44|triplex|duplex|fourplex/i.test(raw) || addr.includes("tantalus")) {
    return "4-Unit Bill 44 Multiplex";
  }
  if (/acreage|estate|meadows/i.test(raw) || addr.includes("pemberton")) {
    return "Custom Acreage Residence";
  }
  if (/alpine|chalet|whistler|single-family|single family/i.test(raw) || addr.includes("alpine")) {
    return "Custom Single-Family Home";
  }
  let cleaned = raw.replace(/\(KP-[^)]+\)/gi, "").replace(/^Custom Build\s*[—-]\s*/i, "").trim();
  if (!cleaned || cleaned.toLowerCase() === String(job.address || "").toLowerCase()) {
    return "Custom Single-Family Home";
  }
  return cleaned;
}

function getJobGeotagCoords(job) {
  const addr = String((job && job.address) || "").toLowerCase();
  if (addr.includes("whistler") || addr.includes("alpine")) {
    return "50.1163° N, 122.9574° W • " + (job.address || "Whistler, BC");
  }
  if (addr.includes("pemberton")) {
    return "50.3210° N, 122.8045° W • " + (job.address || "Pemberton, BC");
  }
  return "49.7361° N, 123.1345° W • " + ((job && job.address) || "40484 Tantalus Rd, Squamish, BC");
}

function buildClean6ConsultantsAnd24Trades(scale) {
  const s = scale || 1.0;
  const r = (n) => Math.round((n * s) / 500) * 500;
  return [
    // --- BOX 1: 6 DISTINCT CONSULTANTS (Each Separate!) ---
    {
      id: 1, phase: "C-01", category: "consultant",
      name: "Architect (AIBC) — Full Architectural Design & IFC Drawings",
      sub: "Studio Vance Architecture AIBC",
      contact: "Marcus Vance, Architect AIBC",
      phone: "(604) 732-8812", email: "mvance@studiovance.ca",
      startDate: "2026-06-01", endDate: "2026-06-19",
      contract: r(38000), billed: r(38000), status: "Completed",
      contractPdf: { name: "C01_Studio_Vance_Architect_AIBC_Signed_Contract.pdf", date: "2026-06-01" },
      revisions: []
    },
    {
      id: 2, phase: "C-02", category: "consultant",
      name: "Structural Engineer (P.Eng.) — Structural Design, Seismic & Schedule B / C-B",
      sub: "Apex Structural Engineering P.Eng.",
      contact: "Elena Rostova, P.Eng.",
      phone: "(604) 689-2210", email: "erostova@apexstructural.ca",
      startDate: "2026-06-05", endDate: "2026-06-22",
      contract: r(24000), billed: r(24000), status: "Completed",
      contractPdf: { name: "C02_Apex_Structural_Engineer_PEng_Signed_Contract.pdf", date: "2026-06-05" },
      revisions: []
    },
    {
      id: 3, phase: "C-03", category: "consultant",
      name: "Geotechnical Engineer (P.Eng.) — Subgrade Bearing, Rock Anchors & Geotech Schedule B",
      sub: "Thurber Geotechnical Engineering Ltd.",
      contact: "Dr. A. Tremblay, P.Eng.",
      phone: "(604) 984-4321", email: "atremblay@thurber.ca",
      startDate: "2026-06-25", endDate: "2026-07-14",
      contract: r(22000), billed: r(22000), status: "Completed",
      contractPdf: { name: "C03_Thurber_Geotechnical_Engineer_Signed_Contract.pdf", date: "2026-06-25" },
      revisions: []
    },
    {
      id: 4, phase: "C-04", category: "consultant",
      name: "Land Surveyor (BCLS) — Property Pinning, Topographic Survey & Foundation Siting",
      sub: "Sea-to-Sky Geomatics & BCLS",
      contact: "Ian McAllister, BCLS",
      phone: "(604) 892-4100", email: "imcallister@seatoskygeomatics.ca",
      startDate: "2026-06-22", endDate: "2026-07-03",
      contract: r(18500), billed: r(18500), status: "Completed",
      contractPdf: { name: "C04_BCLS_Land_Surveyor_Signed_Contract.pdf", date: "2026-06-22" },
      revisions: []
    },
    {
      id: 5, phase: "C-05", category: "consultant",
      name: "Energy Step Code 4 & Zero Carbon Consultant (CEA) — HOT2000 & Blower Door",
      sub: "E3 Eco Group Energy Advisors",
      contact: "Liam O'Connor, CEA",
      phone: "(604) 684-5588", email: "loconnor@e3ecogroup.ca",
      startDate: "2026-07-08", endDate: "2026-07-21",
      contract: r(9500), billed: r(9500), status: "Completed",
      contractPdf: { name: "C05_E3_Energy_Step_Code_Advisor_Signed_Contract.pdf", date: "2026-07-08" },
      revisions: []
    },
    {
      id: 6, phase: "C-06", category: "consultant",
      name: "Building Envelope Engineer (P.Eng.) — Rainscreen, Air Barrier & Window Detailing",
      sub: "Morrison Hershfield Envelope Engineering",
      contact: "David Chen, P.Eng.",
      phone: "(604) 454-0402", email: "dchen@morrisonhershfield.com",
      startDate: "2026-07-15", endDate: "2026-12-10",
      contract: r(14500), billed: r(7500), status: "Active On-Site",
      contractPdf: { name: "C06_Building_Envelope_Engineer_Signed_Contract.pdf", date: "2026-07-15" },
      revisions: []
    },

    // --- BOX 2: 24 SITE TRADES (Start to Finish) ---
    { id: 7, phase: "T-01", category: "trade", name: "Hazardous Materials Abatement, Site Hoarding & Silt Fencing", sub: "Squamish Environmental & Site Prep", contact: "Trevor Vance", phone: "(604) 898-4410", startDate: "2026-07-22", endDate: "2026-07-31", contract: r(22000), billed: r(22000), status: "Completed", revisions: [] },
    { id: 8, phase: "T-02", category: "trade", name: "Land Clearing, Demolition, Stripping & Bulk Excavation", sub: "Alpine Rock Excavation Ltd", contact: "Grant Vance", phone: "(604) 898-3312", startDate: "2026-08-03", endDate: "2026-08-14", contract: r(68000), billed: r(68000), status: "Completed", revisions: [] },
    { id: 9, phase: "T-03", category: "trade", name: "Rock Blasting, Hydraulic Micro-Splitting & Bedrock Anchors", sub: "Tantalus Drilling & Blasting", contact: "Mark Kovacs", phone: "(604) 984-4321", startDate: "2026-08-17", endDate: "2026-08-26", contract: r(44000), billed: r(44000), status: "Completed", revisions: [
      
    ] },
    { id: 10, phase: "T-04", category: "trade", name: "Civil Underground Utilities, Storm Retention & BC Hydro ES54 Ducts", sub: "Sea-to-Sky Civil Works Ltd", contact: "Wayne Stevenson (ES54)", phone: "(604) 848-9688", startDate: "2026-08-27", endDate: "2026-09-08", contract: r(96000), billed: r(96000), status: "Completed", revisions: [] },
    { id: 11, phase: "T-05", category: "trade", name: "Footing & Foundation Formwork + 15M/20M Seismic Rebar Cages", sub: "Black Tusk Formwork & Rebar", contact: "Marco Rossi", phone: "(604) 898-7721", startDate: "2026-09-09", endDate: "2026-09-22", contract: r(112000), billed: r(112000), status: "Completed", revisions: [] },
    { id: 12, phase: "T-06", category: "trade", name: "35 MPa Concrete Placing, Boom Pump & Foundation Wall Pour", sub: "Burnco Concrete & Coastal Placing", contact: "Darren Miller", phone: "(604) 892-5540", startDate: "2026-09-23", endDate: "2026-09-30", contract: r(84000), billed: r(84000), status: "Completed", revisions: [] },
    { id: 13, phase: "T-07", category: "trade", name: "Dampproofing, Dimple Membrane, Weeping Tile & Drain Rock Backfill", sub: "Pacific Shield Waterproofing", contact: "Tyler Vance", phone: "(604) 905-8833", startDate: "2026-10-01", endDate: "2026-10-06", contract: r(32000), billed: r(32000), status: "Completed", revisions: [] },
    { id: 14, phase: "T-08", category: "trade", name: "Underslab Plumbing DWV, Radon Depressurization, XPS & Slab Pour", sub: "Garibaldi Concrete & Sea-to-Sky Plumbing", contact: "Ryan Kowalski", phone: "(604) 898-9011", startDate: "2026-10-07", endDate: "2026-10-10", contract: r(48000), billed: r(48000), status: "Completed", revisions: [] },
    { id: 15, phase: "T-09", category: "trade", name: "Structural Steel Moment Frames, W-Beams, HSS Columns & Crane Hoisting", sub: "Garibaldi Structural Steel Ltd", contact: "Shane O'Connor", phone: "(604) 892-3199", startDate: "2026-10-11", endDate: "2026-10-14", contract: r(95000), billed: r(95000), status: "Completed", revisions: [] },
    { id: 16, phase: "T-10", category: "trade", name: "Rough Wood Framing, TJI Floor Joists, Shear Walls & Roof Trusses", sub: "Pacific Ridge Timberworks Ltd", contact: "Cody MacLeod", phone: "(604) 898-6120", startDate: "2026-10-12", endDate: "2026-11-06", contract: r(285000), billed: r(162000), status: "Active On-Site", revisions: [] },
    { id: 17, phase: "T-11", category: "trade", name: "Standing Seam Metal Roofing & 2-Ply SBS Torch-On Flat Roof Decks", sub: "Whistler Alpine Sheet Metal & Roofing", contact: "Brett Lindqvist", phone: "(604) 932-4490", startDate: "2026-11-09", endDate: "2026-11-20", contract: r(82000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 18, phase: "T-12", category: "trade", name: "Innotech Triple-Pane Tilt-&-Turn Windows & Lift-Slide Patio Doors", sub: "Innotech Windows + Doors BC", contact: "Henrik Lind", phone: "(604) 854-1122", startDate: "2026-11-23", endDate: "2026-12-04", contract: r(118000), billed: r(59000), status: "Scheduled", revisions: [] },
    { id: 19, phase: "T-13", category: "trade", name: "Building Envelope, SIGA Air Barrier, Exterior Insulation & Rainscreen Siding", sub: "Vantage Passive Wall Systems", contact: "Lucas Meyer", phone: "(604) 739-8820", startDate: "2026-12-07", endDate: "2026-12-23", contract: r(134000), billed: 0, status: "Scheduled", revisions: [
      
    ] },
    { id: 20, phase: "T-14", category: "trade", name: "Plumbing Rough-In, Uponor PEX-a Manifold, Gas & Domestic Hot Water", sub: "Sea-to-Sky Mechanical & Plumbing", contact: "Devon Patel", phone: "(604) 892-7741", startDate: "2026-12-14", endDate: "2027-01-05", contract: r(98000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 21, phase: "T-15", category: "trade", name: "Hydronic In-Floor Heating, Mitsubishi VRF Heat Pumps & Zehnder HRV", sub: "North Shore Climate & Hydronics", contact: "jaswinder Gill", phone: "(604) 980-6612", startDate: "2027-01-06", endDate: "2027-01-19", contract: r(92000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 22, phase: "T-16", category: "trade", name: "NFPA 13D Fire Suppression Sprinklers, Standpipes & Life Safety", sub: "Apex Fire Protection BC", contact: "craig Morrison", phone: "(604) 299-5100", startDate: "2027-01-20", endDate: "2027-01-26", contract: r(28000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 23, phase: "T-17", category: "trade", name: "Electrical 400A Service, Rough-In, Lutron Lighting & Dual 80A EV", sub: "Current Energy Electrical Ltd", contact: "Nathan Brooks", phone: "(604) 898-2204", startDate: "2027-01-27", endDate: "2027-02-09", contract: r(104000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 24, phase: "T-18", category: "trade", name: "2lb Closed-Cell Spray Foam, Rockwool Acoustic Batt & Vapour Barrier", sub: "Pacific Thermal Insulation", contact: "kevin Cho", phone: "(604) 435-9910", startDate: "2027-02-10", endDate: "2027-02-18", contract: r(46000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 25, phase: "T-19", category: "trade", name: "5/8\" Type X Fire-Rated Drywall Boarding, Taping & Level 5 Skim Coat", sub: "Pinnacle Drywall & Acoustics", contact: "Carlos Mendez", phone: "(604) 521-7780", startDate: "2027-02-19", endDate: "2027-03-04", contract: r(76000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 26, phase: "T-20", category: "trade", name: "Custom Rift-Sawn White Oak Millwork, Kitchen Cabinetry & Solid Doors", sub: "Squamish Fine Millwork & Joinery", contact: "julian Berg", phone: "(604) 892-1944", startDate: "2027-03-05", endDate: "2027-03-16", contract: r(115000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 27, phase: "T-21", category: "trade", name: "Large-Format Italian Porcelain Tile, Schluter Wet-Zones & Quartz Slabs", sub: "Garibaldi Stone & Tile Artisans", contact: "Enzo Bellini", phone: "(604) 938-2219", startDate: "2027-03-17", endDate: "2027-03-26", contract: r(64000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 28, phase: "T-22", category: "trade", name: "Wide-Plank Engineered White Oak Flooring, Stair Treads & Glass Railings", sub: "Sea-to-Sky Hardwood & Glass", contact: "Paul Stirling", phone: "(604) 898-5050", startDate: "2027-03-29", endDate: "2027-04-06", contract: r(58000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 29, phase: "T-23", category: "trade", name: "Interior & Exterior Zero-VOC Architectural Painting & Wood Stains", sub: "Tantalus Architectural Coatings", contact: "Andre Bouchard", phone: "(604) 892-6300", startDate: "2027-04-07", endDate: "2027-04-14", contract: r(38000), billed: 0, status: "Scheduled", revisions: [] },
    { id: 30, phase: "T-24", category: "trade", name: "Permeable Paver Driveways, Cedar Fencing, Landscaping & Final Walkthrough", sub: "Keystone Possibilities Ltd (#52603) & Coastal Civil", contact: "Wayne Stevenson", phone: "(604) 848-9688", startDate: "2027-04-15", endDate: "2027-04-30", contract: r(64000), billed: 0, status: "Scheduled", revisions: [] }
  ];
}

function buildMasterCityPermitsAndSchedulesVault(job) {
  const muni = resolveJobMunicipality(job);
  const geo = getJobGeotagCoords(job);
  const pNum = job.permitNum || "BP2026-0419";

  return {
    // MASTER BRACKET 1: APPROVED PLANS & LETTERS OF ASSURANCE (SCHEDULE A / B / C-A / C-B)
    plansAndSchedules: [
      { id: "SCH-A", code: "SCHEDULE A", title: "Confirmation of Commitment by Owner & Coordinating Registered Professional (CRP)", firm: "Marcus Vance, Architect AIBC & Wayne Stevenson (#52603)", date: "2026-06-02", status: "SEALED & FILED", pdfName: job.jobId + "_BCBC_Schedule_A_CRP_Signed.pdf" },
      { id: "SCH-B-ARCH", code: "SCHEDULE B (ARCHITECTURAL)", title: "Assurance of Professional Design & Commitment for Field Review — Architectural & Step Code 4", firm: "Studio Vance Architecture AIBC (Marcus Vance)", date: "2026-06-05", status: "SEALED & FILED", pdfName: job.jobId + "_BCBC_Schedule_B_Architectural.pdf" },
      { id: "SCH-B-STRUCT", code: "SCHEDULE B (STRUCTURAL)", title: "Assurance of Professional Design & Field Review — Structural Steel, Seismic Shear Walls & Foundation", firm: "Apex Structural Engineering P.Eng. (Elena Rostova, P.Eng.)", date: "2026-06-08", status: "SEALED & FILED", pdfName: job.jobId + "_BCBC_Schedule_B_Structural_PEng.pdf" },
      { id: "SCH-B-GEO", code: "SCHEDULE B (GEOTECHNICAL)", title: "Assurance of Professional Design & Field Review — Subgrade Excavation, Rock Anchors & 300 kPa Bearing", firm: "Thurber Geotechnical Engineering Ltd. (Dr. A. Tremblay, P.Eng.)", date: "2026-06-28", status: "SEALED & FILED", pdfName: job.jobId + "_BCBC_Schedule_B_Geotechnical_PEng.pdf" },
      { id: "SCH-B-ENV", code: "SCHEDULE B (BUILDING ENVELOPE)", title: "Assurance of Professional Design & Field Review — Rainscreen Assembly, Air Barrier & Fenestration", firm: "Morrison Hershfield Envelope P.Eng. (David Chen, P.Eng.)", date: "2026-07-16", status: "SEALED & FILED", pdfName: job.jobId + "_BCBC_Schedule_B_Envelope_PEng.pdf" },
      { id: "PLAN-IFC-ARCH", code: "IFC ARCHITECTURAL PLANS", title: "City-Stamped Issued for Construction (IFC) Architectural Blueprint Set (Floor Plans, Elevations, Sections)", firm: "Studio Vance Architecture AIBC", date: "2026-06-19", status: "APPROVED BY CITY", pdfName: job.jobId + "_Approved_IFC_Architectural_Plans.pdf" },
      { id: "PLAN-IFC-ENG", code: "IFC STRUCTURAL & CIVIL PLANS", title: "Sealed Structural Framing, Foundation Rebar, Simpson Hold-Downs & Civil Storm Detention Drawings", firm: "Apex Structural P.Eng. & Sea-to-Sky Civil", date: "2026-06-19", status: "APPROVED BY CITY", pdfName: job.jobId + "_Approved_IFC_Structural_Civil_Plans.pdf" },
      { id: "SCH-CA-CB", code: "SCHEDULE C-A & C-B (OCCUPANCY)", title: "Letters of Assurance of Professional Field Review & Compliance (Required Prior to Final Occupancy)", firm: "CRP Architect AIBC + Structural, Geotech & Envelope P.Eng.", date: "2027-04-20", status: "IN PROGRESS", pdfName: job.jobId + "_BCBC_Schedule_CA_CB_Occupancy_Pack.pdf" }
    ],

    // MASTER BRACKET 2: MUNICIPAL & TRADE PERMITS PULLED
    permitsMade: [
      { id: "PRM-BLD", code: "BUILDING PERMIT #" + pNum, title: muni + " Master Building Permit (4-Unit Bill 44 Multiplex / Custom Residence)", authority: muni + " Building Department", date: "2026-06-19", status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_Building_Permit_" + pNum + ".pdf" },
      { id: "PRM-ESC", code: "ESC & EARTHWORKS PERMIT #ESC-2026-118", title: "Erosion & Sediment Control (ESC), Tree Protection & Bulk Excavation Permit", authority: muni + " Engineering & Environmental", date: "2026-07-20", status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_ESC_Earthworks_Permit.pdf" },
      { id: "PRM-CIV", code: "CIVIL & BC HYDRO ES54 #ES54-8841", title: "Municipal Water/Sewer Connection, Storm Detention Chamber & BC Hydro ES54 Primary Duct Permit", authority: muni + " Civil & BC Hydro", date: "2026-08-25", status: "PERMIT ISSUED & PASSED", pdfName: job.jobId + "_Civil_BCHydro_ES54_Permit.pdf" },
      { id: "PRM-PLM", code: "PLUMBING & RADON PERMIT #PLM-2026-409", title: "Municipal DWV Underslab Plumbing, Domestic Water & Radon Mitigation Permit", authority: muni + " Plumbing Inspector", date: "2026-10-02", status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_Plumbing_Permit_PLM409.pdf" },
      { id: "PRM-ELC", code: "ELECTRICAL 400A PERMIT #ELC-2026-992", title: "Technical Safety BC / Municipal 400A Underground Service & EVEMS Electrical Permit", authority: "Technical Safety BC & " + muni, date: "2026-10-10", status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_Electrical_Permit_ELC992.pdf" },
      { id: "PRM-GAS", code: "MECHANICAL & HVAC PERMIT #MCH-2026-512", title: "Hydronic Radiant Floor, VRF Heat Pump & Zehnder HRV Ventilation Permit", authority: muni + " Mechanical Inspector", date: "2026-10-14", status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_Mechanical_HVAC_Permit.pdf" }
    ],

    // MASTER BRACKET 3: ALL INSPECTION REPORTS UNDERNEATH (CITY & ENGINEERING FIELD REVIEWS)
    inspectionReports: [
      { id: "RPT-01", code: "INSP-01 • BCLS SITING", title: "BCLS Pinning, Setback Verification & SPEA Tree Barrier Inspection Report", authority: "Ian McAllister, BCLS & " + muni, trade: "Sea-to-Sky Geomatics (C-04)", date: "2026-07-03", geotag: geo, status: "PASSED", notes: "All property corners pinned and tree protection hoarding verified prior to excavation.", pdfName: "Report_01_BCLS_Siting_Passed.pdf" },
      { id: "RPT-02", code: "INSP-02 • GEOTECH BEARING", title: "Geotechnical Subgrade Stripping, Rock Bolts & 300 kPa Footing Bearing Field Report", authority: "Dr. A. Tremblay, P.Eng. (Thurber Geotech)", trade: "Thurber Geotech (C-03) & Tantalus Blasting (T-03)", date: "2026-08-26", geotag: geo, status: "PASSED", notes: "Competent granodiorite bedrock confirmed at 300 kPa allowable bearing pressure.", pdfName: "Report_02_Thurber_Geotech_Bearing_Passed.pdf" },
      { id: "RPT-03", code: "INSP-03 • BC HYDRO ES54 & CIVIL", title: "Underground Storm Retention, Sanitary/Water & BC Hydro ES54 Mandrel Inspection Report", authority: muni + " Civil & BC Hydro Inspector", trade: "Sea-to-Sky Civil Works (T-04)", date: "2026-09-08", geotag: geo, status: "PASSED", notes: "75mm ducts mandrel-tested, warning tape & tracer wire verified prior to backfill.", pdfName: "Report_03_Civil_BCHydro_ES54_Passed.pdf" },
      { id: "RPT-04", code: "INSP-04 • FOOTING & REBAR", title: "Foundation Formwork, 15M/20M Seismic Rebar & Hold-Down Anchor Field Review Report", authority: "Elena Rostova, P.Eng. (Apex Structural) & " + muni, trade: "Black Tusk Formwork & Rebar (T-05)", date: "2026-09-22", geotag: geo, status: "PASSED", notes: "All seismic stirrups, lap splices, and Simpson PAB anchor bolts approved for concrete pour.", pdfName: "Report_04_Footing_Rebar_Passed.pdf" },
      { id: "RPT-05", code: "INSP-05 • DAMPPROOFING & DRAIN", title: "Foundation Dampproofing, Dimple Membrane, Weeping Tile & Crush Rock Inspection Report", authority: muni + " Building Inspector", trade: "Pacific Shield Waterproofing (T-07)", date: "2026-10-06", geotag: geo, status: "PASSED", notes: "Perimeter drainage slope, filter cloth, and dampproofing termination bar passed.", pdfName: "Report_05_Dampproofing_DrainTile_Passed.pdf" },
      { id: "RPT-06", code: "INSP-06 • UNDERSLAB & RADON", title: "Underslab DWV Plumbing Pressure Test, Radon Rock Pit & Vapour Barrier Inspection Report", authority: muni + " Plumbing & Building Inspector", trade: "Garibaldi Concrete & Sea-to-Sky Plumbing (T-08)", date: "2026-10-10", geotag: geo, status: "PASSED", notes: "10ft head test held 100%; 4\" perforated radon collector pipe & 15-mil Stego wrap approved.", pdfName: "Report_06_Underslab_Plumbing_Radon_Passed.pdf" },
      { id: "RPT-07", code: "INSP-07 • STRUCTURAL STEEL", title: "Structural Steel Moment Frames, Welds & High-Strength Bolt Torque Field Review Report", authority: "Elena Rostova, P.Eng. (Apex Structural)", trade: "Garibaldi Structural Steel (T-09)", date: "2026-10-14", geotag: geo, status: "PASSED", notes: "All W-beam connections and baseplate grouting certified under Schedule B.", pdfName: "Report_07_Structural_Steel_ScheduleB_Passed.pdf" },
      { id: "RPT-08", code: "INSP-08 • ROUGH FRAMING & SHEAR", title: "Wood Framing, Shear Wall Nailing, HDU8 Hold-Downs & Roof Truss Bearing Inspection", authority: muni + " Building Inspector & Apex Structural P.Eng.", trade: "Pacific Ridge Timberworks (T-10)", date: "2026-11-05", geotag: geo, status: "SCHEDULED / ACTIVE", notes: "Verify 3\" edge nailing on gridlines B & D and install remaining HDU8 hold-down nuts prior to City Framing Inspection.", pdfName: "Report_08_Framing_ShearWall_Checklist.pdf" }
    ]
  };
}

const _origEnsure30Trades = ensureArchitectToFinish22Trades;
ensureArchitectToFinish22Trades = function(job) {
  if (!job) return;
  const s = (job.contractPrice && job.contractPrice > 2500000) ? (job.contractPrice / 1850000) : 1.0;

  // Upgrade to the clean 6 Consultants + 24 Trades if not yet upgraded to v13
  if (!Array.isArray(job.trades) || job.trades.length < 30 || !String(job.trades[0].phase || "").startsWith("C-")) {
    job.trades = buildClean6ConsultantsAnd24Trades(s);
  }

  if (!job.cityMasterVault) {
    job.cityMasterVault = buildMasterCityPermitsAndSchedulesVault(job);
  }

  const geo = getJobGeotagCoords(job);
  (job.trades || []).forEach((tr, idx) => {
    if (!tr.id) tr.id = idx + 1;
    if (!tr.category) {
      tr.category = String(tr.phase || "").startsWith("C-") ? "consultant" : "trade";
    }
    if (!tr.contact) tr.contact = tr.category === "consultant" ? "Principal P.Eng. / Architect" : "Site Foreman";
    if (!tr.phone) tr.phone = "(604) 848-9688";
    if (!tr.email) {
      const slug = String(tr.sub || "partner").toLowerCase().replace(/[^a-z0-9]+/g, "").slice(0, 14) || "partner";
      tr.email = "dispatch@" + slug + ".ca";
    }
    if (!tr.contractPdf || typeof tr.contractPdf !== "object") {
      tr.contractPdf = {
        name: tr.phase + "_" + String(tr.sub || "Partner").replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 22) + "_Signed_Contract.pdf",
        date: tr.startDate || "2026-06-01",
        ownerSigned: true,
        ownerSignedBy: job.ownerName || "Property Owner",
        dataUrl: ""
      };
    }

    // Partner's Dedicated Page Files:
    // 1) Signed Contract PDF
    // 2) Change Orders
    // 3) Plans, Drawings & Specifications (Upload/Download)
    if (!Array.isArray(tr.partnerPlans) || tr.partnerPlans.length === 0) {
      if (tr.category === "consultant") {
        tr.partnerPlans = [
          {
            id: "PLN-" + tr.phase + "-01",
            title: "Issued for Construction (IFC) Plans, Sealed Drawings & Schedule B Package — " + tr.sub,
            rev: "Rev 3 — Latest Sealed Set",
            date: tr.endDate || tr.startDate || "2026-06-19",
            pdfName: tr.phase + "_" + String(tr.sub || "Consultant").replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 20) + "_Plans_Set.pdf",
            dataUrl: ""
          }
        ];
      } else {
        tr.partnerPlans = [
          {
            id: "PLN-" + tr.phase + "-01",
            title: "Shop Drawings, Trade Scope Plans & Field Specification Sheet — " + tr.sub,
            rev: "IFC Field Set",
            date: tr.startDate || "2026-08-01",
            pdfName: tr.phase + "_" + String(tr.sub || "Trade").replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 20) + "_Shop_Plans.pdf",
            dataUrl: ""
          }
        ];
      }
    }
  });
};

(portalStore.jobs || []).forEach(j => ensureArchitectToFinish22Trades(j));

// ============================================================================
// 1. LOGIN GATE vs. LOGGED-IN TOP HEADER BAR
// ============================================================================
renderJobSelectors = function() {
  const loginSel = document.getElementById("ks-job-select");
  const hdrSel = document.getElementById("kp-header-job-select");
  const activeJob = getActiveJob();

  if (loginSel) {
    loginSel.innerHTML = (portalStore.jobs || []).map(j => {
      const propType = getCleanPropertyTypeLabel(j);
      return `<option value="${escapeHtml(j.jobId)}" ${j.jobId === activeJob.jobId ? "selected" : ""}>${escapeHtml(j.address)} — ${escapeHtml(propType)}</option>`;
    }).join("");
  }
  if (hdrSel) {
    hdrSel.style.setProperty("display", "none", "important");
  }
  const staticTitle = document.getElementById("kp-header-static-job-title");
  if (staticTitle && activeJob) staticTitle.innerText = activeJob.address;
  const staticSub = document.getElementById("kp-header-static-job-sub");
  if (staticSub && activeJob) staticSub.innerText = getCleanPropertyTypeLabel(activeJob);

  const clientInput = document.getElementById("ks-client-id");
  if (clientInput && activeJob && !clientInput.value) clientInput.value = activeJob.address;
};

const _origRenderTab1Contract = renderTab1Contract;
renderTab1Contract = function() {
  _origRenderTab1Contract();
  const job = getActiveJob();
  const staticTitle = document.getElementById("kp-header-static-job-title");
  if (staticTitle && job) staticTitle.innerText = job.address;
  const staticSub = document.getElementById("kp-header-static-job-sub");
  if (staticSub && job) staticSub.innerText = getCleanPropertyTypeLabel(job);
  const hdrSel = document.getElementById("kp-header-job-select");
  if (hdrSel) hdrSel.style.setProperty("display", "none", "important");
};

// ============================================================================
// 2. TAB 2: LIVE CALENDAR UPDATES (Start Date / Expected End Date / Change Order Days Over)
// ============================================================================
function getJobScheduleSummary(job) {
  ensureArchitectToFinish22Trades(job);
  const trades = job.trades || [];
  const startDate = job.projectStartDate || (trades[0] && trades[0].startDate) || "2026-06-01";
  const expectedEndDate = job.expectedEndDate || (trades[trades.length - 1] && trades[trades.length - 1].endDate) || "2027-04-30";

  let coDays = 0;
  let coCount = 0;
  trades.forEach(tr => {
    (tr.revisions || []).forEach(rv => {
      if (rv.signed && Number(rv.days)) {
        coDays += Number(rv.days) || 0;
        coCount++;
      }
    });
  });

  let revisedEndDate = expectedEndDate;
  try {
    const dt = new Date(expectedEndDate + "T12:00:00");
    if (!isNaN(dt.getTime())) {
      dt.setDate(dt.getDate() + coDays);
      revisedEndDate = dt.toISOString().slice(0, 10);
    }
  } catch (e) {}

  return { startDate, expectedEndDate, coDays, coCount, revisedEndDate };
}

function updateProjectBaselineDates(field, val) {
  const job = getActiveJob();
  if (!job || !val) return;
  if (field === "start") job.projectStartDate = val;
  if (field === "end") job.expectedEndDate = val;
  saveState();
  renderCalendar();
  showToast("Updated Project Baseline Schedule Date");
}

const _origRenderCalendar = renderCalendar;
renderCalendar = function() {
  _origRenderCalendar();
  const job = getActiveJob();
  const sched = getJobScheduleSummary(job);

  let bracketEl = document.getElementById("p2-project-timeline-bracket");
  if (!bracketEl) {
    const calGrid = document.getElementById("kp-calendar-days");
    if (calGrid && calGrid.parentNode) {
      bracketEl = document.createElement("div");
      bracketEl.id = "p2-project-timeline-bracket";
      bracketEl.style.cssText = "margin-top:14px; padding:12px 16px; background:linear-gradient(180deg, rgba(212,175,55,0.10) 0%, #060a12 100%); border:1px solid rgba(212,175,55,0.45); border-radius:12px; display:grid; grid-template-columns:repeat(4, minmax(0, 1fr)); gap:12px; align-items:center;";
      calGrid.parentNode.appendChild(bracketEl);
    }
  }

  if (bracketEl) {
    const overLabel = sched.coDays > 0
      ? `+${sched.coDays} Days Over (${sched.coCount} Change Order${sched.coCount === 1 ? "" : "s"})`
      : "0 Days Over (On Original Schedule)";
    bracketEl.innerHTML = `
      <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:9px 12px;">
        <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">1. Project Start Date</div>
        <input type="date" value="${escapeHtml(sched.startDate)}" onchange="updateProjectBaselineDates('start', this.value)" style="background:transparent; border:none; color:#ffffff; font-size:0.98rem; font-weight:900; margin-top:3px; padding:0; outline:none; color-scheme:dark; cursor:pointer; width:100%;" />
        <div style="font-size:0.68rem; color:#94a3b8;">Project Mobilization</div>
      </div>

      <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:9px 12px;">
        <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">2. Original Expected End Date</div>
        <input type="date" value="${escapeHtml(sched.expectedEndDate)}" onchange="updateProjectBaselineDates('end', this.value)" style="background:transparent; border:none; color:#ffffff; font-size:0.98rem; font-weight:900; margin-top:3px; padding:0; outline:none; color-scheme:dark; cursor:pointer; width:100%;" />
        <div style="font-size:0.68rem; color:#94a3b8;">Baseline Contract Completion</div>
      </div>

      <div style="background:#05070b; border:1px solid rgba(212,175,55,0.45); border-radius:10px; padding:9px 12px;">
        <div style="font-size:0.65rem; font-weight:800; color:#f3e5ab; text-transform:uppercase; letter-spacing:0.06em;">3. Change Order Days Over</div>
        <div style="font-size:0.98rem; font-weight:900; color:#d4af37; margin-top:3px;">${escapeHtml(overLabel)}</div>
        <div style="font-size:0.68rem; color:#f3e5ab;">Auto-Synced from Change Orders</div>
      </div>

      <div style="background:#05070b; border:1.5px solid #d4af37; border-radius:10px; padding:9px 12px;">
        <div style="font-size:0.65rem; font-weight:800; color:#d4af37; text-transform:uppercase; letter-spacing:0.06em;">4. New Expected Completion Date</div>
        <div style="font-size:1.02rem; font-weight:900; color:#ffffff; margin-top:3px;">${escapeHtml(sched.revisedEndDate)}</div>
        <div style="font-size:0.68rem; color:#d4af37;">${sched.coDays > 0 ? ("Includes +" + sched.coDays + " Days from Change Orders") : "On Time with Baseline Contract"}</div>
      </div>
    `;
  }
};

renderActiveTradeRadar = function() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const activeListEl = document.getElementById("p2-active-trades-list");
  if (!activeListEl) return;

  const daysInMonth = new Date(calYear, calMonth + 1, 0).getDate();
  const monthStart = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-01`;
  const monthEnd = `${calYear}-${String(calMonth + 1).padStart(2, "0")}-${String(daysInMonth).padStart(2, "0")}`;
  const monthLabel = `${KP_MONTH_NAMES[calMonth] || "October"} ${calYear}`;

  const mBadge = document.getElementById("p2-active-trades-month-badge");
  if (mBadge) mBadge.innerText = monthLabel.toUpperCase();
  const mHead = document.getElementById("p2-active-trades-heading");
  if (mHead) mHead.innerText = `Scheduled Consultants & Trades in ${monthLabel}`;

  const monthlyTrades = (job.trades || []).filter(t =>
    t.startDate && t.endDate && t.startDate <= monthEnd && t.endDate >= monthStart
  );

  const countBadge = document.getElementById("p2-active-trades-count");
  if (countBadge) {
    countBadge.innerText = `${monthlyTrades.length} Active in ${monthLabel}`;
  }

  if (!monthlyTrades.length) {
    activeListEl.innerHTML = `
      <div style="background:#0b0f17; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:14px 16px; color:#cbd5e1; font-size:0.82rem;">
        No consultants or trades scheduled in ${escapeHtml(monthLabel)}. Select another month above.
      </div>
    `;
    return;
  }

  activeListEl.innerHTML = monthlyTrades.map(t => {
    return `
      <div onclick="switchPortalPage(4); openP4TradeDetailPage(${t.id});" style="background:#080c14; border:1px solid rgba(212,175,55,0.32); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:10px; cursor:pointer;">
        <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1;">
          <span class="kp-badge-pill kp-badge-gold">${escapeHtml(t.phase)}</span>
          <div style="font-size:0.86rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            ${escapeHtml(t.name)} &mdash; <span style="color:#f3e5ab;">${escapeHtml(t.contact)} (${escapeHtml(t.sub)})</span>
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:14px; flex-shrink:0;">
          <span style="font-size:0.76rem; color:#cbd5e1;">${escapeHtml(t.startDate)} &rarr; ${escapeHtml(t.endDate)}</span>
          <span style="font-size:0.76rem; color:#d4af37; font-weight:900;">Signed Contract: ${fmtMoney(t.contract)}</span>
          <span class="kp-secondary-btn kp-pill-sm">Open &rarr;</span>
        </div>
      </div>
    `;
  }).join("");
};

// ============================================================================
// 3. TAB 3: THE 3-BOX MASTER BREAKDOWN
//    - TOP BOX (BOX 1): CONSULTANTS (Architect, Structural Eng, Geotech, BCLS Survey, Step Code, Envelope)
//    - MIDDLE BOX (BOX 2): TRADES (Trade Name, Person We're Working With, Signed Contract)
//    - BOTTOM BOX (BOX 3): CITY INSPECTIONS, PERMITS & SCHEDULES (Schedule A, Schedule B, C-A, C-B)
// ============================================================================
openP4TradeDetailPage = function(tradeId) {
  selectedP4TradeId = Number(tradeId);
  selectedP4ViewMode = "partner";
  renderTradesList();
  window.scrollTo({ top: 0, behavior: "smooth" });
};

closeP4TradeDetailPage = function() {
  selectedP4TradeId = null;
  selectedP4ViewMode = "list";
  renderTradesList();
  window.scrollTo({ top: 0, behavior: "smooth" });
};

function openP4CityMasterPage(focusSection) {
  selectedP4TradeId = null;
  selectedP4ViewMode = "city_master";
  renderTradesList();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderConsultantOrTradeRow(t) {
  const cAmt = Number(t.contract) || 0;
  const coSum = (t.revisions || []).filter(r => r.signed).reduce((s, r) => s + (Number(r.amount) || 0), 0);
  const totalContract = cAmt + coSum;

  return `
    <div class="kp-p4-trade-row" onclick="openP4TradeDetailPage(${t.id})" style="display:flex !important; justify-content:space-between !important; align-items:center !important; gap:12px !important; flex-wrap:nowrap !important; padding:10px 14px !important;">
      <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1.4;">
        <span class="kp-badge-pill kp-badge-gold" style="flex-shrink:0;">${escapeHtml(t.phase)}</span>
        <div style="min-width:0; flex:1;">
          <div style="font-size:0.87rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            ${escapeHtml(t.name)}
          </div>
          <div style="font-size:0.74rem; color:#cbd5e1; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            Working With: <strong style="color:#f3e5ab;">${escapeHtml(t.contact || "Project Lead")}</strong> (${escapeHtml(t.sub)}) &bull; ${escapeHtml(t.phone || "(604) 848-9688")}
          </div>
        </div>
      </div>

      <div style="display:flex; align-items:center; gap:16px; flex-shrink:0; white-space:nowrap;">
        <span style="font-size:0.78rem; color:#cbd5e1;">
          Signed Contract: <strong style="color:#d4af37; font-size:0.88rem;">${fmtMoney(totalContract)}</strong>
        </span>
        <span style="font-size:0.75rem; color:#cbd5e1;">
          ${escapeHtml(t.startDate || "TBD")} &rarr; ${escapeHtml(t.endDate || "TBD")}
        </span>
        <button type="button" onclick="event.stopPropagation(); openP4TradeDetailPage(${t.id})" class="kp-secondary-btn kp-pill-sm">
          Open Page &rarr;
        </button>
      </div>
    </div>
  `;
}

function promptQuickAddConsultantOrTrade(category) {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const isCons = category === "consultant";
  const label = isCons ? "Consultant (e.g. Architect, Structural Engineer, Geotech, BCLS)" : "Trade";

  const name = prompt(`Enter ${label} Name / Scope:`, isCons ? "Acoustic & Mechanical Engineer (P.Eng.)" : "Custom Timber Framing & Decking");
  if (!name) return;
  const contact = prompt("Enter the Person We Are Working With (Name):", isCons ? "Dr. S. Bennett, P.Eng." : "Mike Miller");
  if (!contact) return;
  const sub = prompt("Enter Company / Firm Name:", isCons ? "Bennett Engineering Group" : "Sea-to-Sky Contracting Ltd.");
  if (!sub) return;
  const contract = Number(prompt("Enter Signed Contract Amount ($ CAD):", "0")) || 0;
  const startDate = prompt("Enter Start Date (YYYY-MM-DD):", "2026-10-25") || "2026-10-25";
  const endDate = prompt("Enter Finish Date (YYYY-MM-DD):", "2026-11-15") || "2026-11-15";

  const consCount = (job.trades || []).filter(x => x.category === "consultant").length;
  const trdCount = (job.trades || []).filter(x => x.category !== "consultant").length;
  const nextId = (job.trades || []).reduce((m, x) => Math.max(m, Number(x.id) || 0), 0) + 1;
  const nextPhase = isCons
    ? ("C-" + String(consCount + 1).padStart(2, "0"))
    : ("T-" + String(trdCount + 1).padStart(2, "0"));

  const newRec = {
    id: nextId,
    phase: nextPhase,
    category: isCons ? "consultant" : "trade",
    name: name.trim(),
    sub: sub.trim(),
    contact: contact.trim(),
    phone: "(604) 848-9688",
    email: "dispatch@" + sub.toLowerCase().replace(/[^a-z0-9]+/g, "").slice(0, 14) + ".ca",
    startDate: startDate.trim(),
    endDate: endDate.trim(),
    contract: contract,
    billed: 0,
    status: "Scheduled",
    contractPdf: {
      name: nextPhase + "_" + sub.trim().replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 20) + "_Signed_Contract.pdf",
      date: startDate.trim(),
      ownerSigned: true,
      ownerSignedBy: job.ownerName || "Property Owner",
      dataUrl: ""
    },
    revisions: [],
    partnerPlans: []
  };

  if (isCons) {
    // Insert right after the last consultant
    const lastConsIdx = (job.trades || []).map(x => x.category).lastIndexOf("consultant");
    if (lastConsIdx >= 0) job.trades.splice(lastConsIdx + 1, 0, newRec);
    else job.trades.unshift(newRec);
  } else {
    job.trades.push(newRec);
  }

  ensureArchitectToFinish22Trades(job);
  saveState();
  renderAllPortalComponents();
  showToast(`Added ${isCons ? "Consultant" : "Trade"}: ${name.trim()} (${contact.trim()})`);
}

renderTradesList = function() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);

  // Hide old top header / KPI grid so Tab 3 shows the clean 3-Box structure immediately
  const topKpiGrid = document.querySelector("#kp-page-4 .kp-metric-grid");
  if (topKpiGrid) topKpiGrid.style.setProperty("display", "none", "important");
  const topHeaderRow = document.querySelector("#kp-page-4 .kp-section-top-row");
  if (topHeaderRow) topHeaderRow.style.setProperty("display", "none", "important");

  const listView = document.getElementById("p4-master-trades-list-view");
  const detailView = document.getElementById("p4-trade-detail-view");
  if (!listView || !detailView) return;

  // Mode A: Dedicated Consultant or Trade Page
  if (selectedP4ViewMode === "partner" && selectedP4TradeId !== null) {
    const activeTr = (job.trades || []).find(t => Number(t.id) === Number(selectedP4TradeId));
    if (activeTr) {
      listView.style.display = "none";
      detailView.style.display = "block";
      renderSelectedTrade3SectionPage(job, activeTr);
      return;
    }
    selectedP4TradeId = null;
    selectedP4ViewMode = "list";
  }

  // Mode B: Master City Inspections, Permits & Schedules Page (3 Master Brackets)
  if (selectedP4ViewMode === "city_master") {
    listView.style.display = "none";
    detailView.style.display = "block";
    renderMasterCityPermitsAndInspectionsPage(job);
    return;
  }

  // Mode C: Main 3-Box View (1. Consultants | 2. Trades | 3. City Inspections, Permits & Schedules)
  listView.style.display = "block";
  detailView.style.display = "none";

  const consultants = (job.trades || []).filter(t => t.category === "consultant");
  const siteTrades = (job.trades || []).filter(t => t.category !== "consultant");
  const consTotal = consultants.reduce((s, t) => s + (Number(t.contract) || 0), 0);
  const tradesTotal = siteTrades.reduce((s, t) => s + (Number(t.contract) || 0), 0);

  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const schCnt = (cm.plansAndSchedules || []).length;
  const prmCnt = (cm.permitsMade || []).length;
  const rptCnt = (cm.inspectionReports || []).length;

  listView.innerHTML = `
    <!-- ===================================================================
         TOP BOX (BOX 1): CONSULTANTS (Architect, Structural Eng, Geotech, BCLS, Step Code, Envelope)
         =================================================================== -->
    <div style="background:#070b12; border:1.5px solid rgba(212,175,55,0.48); border-radius:14px; padding:14px 16px; margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="kp-badge-pill kp-badge-gold">BOX 1 &bull; CONSULTANTS</span>
            <span class="kp-badge-pill kp-badge-white">${consultants.length} Consultants &bull; Signed Contracts: ${fmtMoney(consTotal)}</span>
          </div>
          <h3 style="font-size:1.02rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            Architect (AIBC), Structural Engineer (P.Eng.), Geotechnical Engineer (P.Eng.), BCLS Surveyor &amp; Step Code
          </h3>
        </div>
        <button type="button" onclick="promptQuickAddConsultantOrTrade('consultant')" class="kp-gold-btn kp-pill-sm">
          + Add Consultant
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${consultants.map(t => renderConsultantOrTradeRow(t)).join("")}
      </div>
    </div>

    <!-- ===================================================================
         MIDDLE BOX (BOX 2): SITE TRADES (Name, Person Working With & Signed Contract)
         =================================================================== -->
    <div style="background:#070b12; border:1.5px solid rgba(212,175,55,0.48); border-radius:14px; padding:14px 16px; margin-bottom:16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="kp-badge-pill kp-badge-gold">BOX 2 &bull; TRADES</span>
            <span class="kp-badge-pill kp-badge-white">${siteTrades.length} Trades &bull; Signed Contracts: ${fmtMoney(tradesTotal)}</span>
          </div>
          <h3 style="font-size:1.02rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            Project Trades, Person We Are Working With &amp; Signed Trade Contracts
          </h3>
        </div>
        <button type="button" onclick="promptQuickAddConsultantOrTrade('trade')" class="kp-gold-btn kp-pill-sm">
          + Add Trade
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${siteTrades.map(t => renderConsultantOrTradeRow(t)).join("")}
      </div>
    </div>

    <!-- ===================================================================
         BOTTOM BOX (BOX 3): CITY INSPECTIONS, PERMITS & SCHEDULES (Schedule A, Schedule B, C-A, C-B)
         Click to open Master Page with 3 Master Brackets: Plans/Schedules, Permits Made, Inspection Reports
         =================================================================== -->
    <div style="background:#070b12; border:1.5px solid #d4af37; border-radius:14px; padding:14px 16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="kp-badge-pill kp-badge-gold">BOX 3 &bull; CITY INSPECTIONS, PERMITS &amp; SCHEDULES (A / B / C-A / C-B)</span>
            <span class="kp-badge-pill kp-badge-white">${schCnt} Plans &amp; Schedules &bull; ${prmCnt} Permits &bull; ${rptCnt} Inspection Reports</span>
          </div>
          <h3 style="font-size:1.02rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            City Permits, Schedule A / Schedule B / Schedule C-B Assurances &amp; All Inspection Reports (Click Any Row to Open Master Vault)
          </h3>
        </div>
        <button type="button" onclick="openP4CityMasterPage()" class="kp-gold-btn kp-pill-sm">
          Open Master Plans, Permits &amp; Inspections Page &rarr;
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        <div class="kp-p4-trade-row" onclick="openP4CityMasterPage('plans')" style="display:flex !important; justify-content:space-between !important; align-items:center !important; gap:12px !important; padding:10px 14px !important;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span class="kp-badge-pill kp-badge-gold">BRACKET 1</span>
            <div>
              <div style="font-size:0.87rem; font-weight:800; color:#ffffff;">Master Approved Plans &amp; BCBC Letters of Assurance (Schedule A, Schedule B, Schedule C-A, Schedule C-B)</div>
              <div style="font-size:0.74rem; color:#cbd5e1;">Architectural IFC Plans, Structural/Geotech Sealed Drawings, Schedule A (CRP), Schedule B &amp; Schedule C-B</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px; flex-shrink:0;">
            <span class="kp-badge-pill kp-badge-white">${schCnt} Master Files</span>
            <button type="button" class="kp-secondary-btn kp-pill-sm">Open Master Plans &amp; Schedules &rarr;</button>
          </div>
        </div>

        <div class="kp-p4-trade-row" onclick="openP4CityMasterPage('permits')" style="display:flex !important; justify-content:space-between !important; align-items:center !important; gap:12px !important; padding:10px 14px !important;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span class="kp-badge-pill kp-badge-gold">BRACKET 2</span>
            <div>
              <div style="font-size:0.87rem; font-weight:800; color:#ffffff;">Municipal &amp; Trade Permits Pulled (Building Permit #${escapeHtml(job.permitNum || "BP2026-0419")}, Plumbing, Electrical, Mechanical, Civil ES54)</div>
              <div style="font-size:0.74rem; color:#cbd5e1;">All active municipal permits and trade permits issued for ${escapeHtml(job.address)}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px; flex-shrink:0;">
            <span class="kp-badge-pill kp-badge-white">${prmCnt} Active Permits</span>
            <button type="button" class="kp-secondary-btn kp-pill-sm">Open Permits Pulled &rarr;</button>
          </div>
        </div>

        <div class="kp-p4-trade-row" onclick="openP4CityMasterPage('reports')" style="display:flex !important; justify-content:space-between !important; align-items:center !important; gap:12px !important; padding:10px 14px !important;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span class="kp-badge-pill kp-badge-gold">BRACKET 3</span>
            <div>
              <div style="font-size:0.87rem; font-weight:800; color:#ffffff;">All City &amp; Engineering Inspection Reports Underneath (Geotagged Field Reports &amp; Deficiencies)</div>
              <div style="font-size:0.74rem; color:#cbd5e1;">BCLS Siting, Geotech Bearing, Footing/Rebar, Dampproofing, Underslab, Structural Steel, Framing &amp; Final Occupancy</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:12px; flex-shrink:0;">
            <span class="kp-badge-pill kp-badge-white">${rptCnt} Inspection Reports</span>
            <button type="button" class="kp-secondary-btn kp-pill-sm">Open Inspection Reports &rarr;</button>
          </div>
        </div>
      </div>
    </div>
  `;
};

// ============================================================================
// WHEN YOU CLICK ON A CONSULTANT (BOX 1) OR TRADE (BOX 2):
// Opens their clean dedicated page with:
//   - Top Bar: Name, Person We're Working With, Signed Contract, Start/Finish Dates
//   - Bracket 1: Signed Contract PDF (Open, Download, Upload New Contract PDF)
//   - Bracket 2: Change Orders (Upload/Add Change Order, Open PDF, Download PDF)
//   - Bracket 3: Plans, Drawings & Trade Specs (Upload New Plans PDF, Open PDF, Download PDF)
// ============================================================================
renderSelectedTrade3SectionPage = function(job, t) {
  ensureArchitectToFinish22Trades(job);
  const detailView = document.getElementById("p4-trade-detail-view");
  if (!detailView) return;

  const isCons = t.category === "consultant";
  const baseContract = Number(t.contract) || 0;
  const revs = t.revisions || [];
  const coSum = revs.filter(r => r.signed).reduce((s, r) => s + (Number(r.amount) || 0), 0);
  const totalContract = baseContract + coSum;
  const cPdf = t.contractPdf || { name: t.phase + "_Signed_Contract.pdf", date: t.startDate || "2026-06-01" };
  const plans = t.partnerPlans || [];

  detailView.innerHTML = `
    <!-- TOP HEADER: BACK BUTTON + PERSON WORKING WITH + SIGNED CONTRACT -->
    <div style="background:#080c14; border:1.5px solid #d4af37; border-radius:12px; padding:13px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <button type="button" onclick="closeP4TradeDetailPage()" class="kp-gold-btn kp-pill-sm">
          &larr; Back to Consultants, Trades &amp; City Permits
        </button>
        <span class="kp-badge-pill kp-badge-white">${isCons ? 'CONSULTANT' : 'TRADE'} &bull; ${escapeHtml(t.phase)}</span>
        <div>
          <h3 style="font-size:1.02rem; font-weight:900; color:#ffffff; margin:0;">
            ${escapeHtml(t.name)}
          </h3>
          <div style="font-size:0.76rem; color:#cbd5e1; margin-top:2px;">
            Person Working With: <strong style="color:#d4af37;">${escapeHtml(t.contact)}</strong> (${escapeHtml(t.sub)}) &bull; 📞 ${escapeHtml(t.phone || "(604) 848-9688")} &bull; ✉️ ${escapeHtml(t.email)}
          </div>
        </div>
      </div>

      <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <div style="background:#05070b; border:1px solid rgba(212,175,55,0.48); border-radius:9px; padding:6px 12px;">
          <div style="font-size:0.62rem; font-weight:800; color:#f3e5ab; text-transform:uppercase;">Signed Contract</div>
          <div style="font-size:1.02rem; font-weight:900; color:#d4af37;">${fmtMoney(totalContract)}</div>
        </div>
        <div style="background:#05070b; border:1px solid rgba(255,255,255,0.16); border-radius:9px; padding:6px 12px;">
          <div style="font-size:0.62rem; font-weight:800; color:#cbd5e1; text-transform:uppercase;">Schedule</div>
          <div style="font-size:0.86rem; font-weight:900; color:#ffffff;">${escapeHtml(t.startDate)} &rarr; ${escapeHtml(t.endDate)}</div>
        </div>
        <button type="button" onclick="promptEditPartnerDetails(${t.id})" class="kp-secondary-btn kp-pill-sm">
          Edit Details / Contract
        </button>
      </div>
    </div>

    <!-- 1. SIGNED CONTRACT PDF (UPLOAD & DOWNLOAD) -->
    <div style="background:#080c14; border:1px solid rgba(212,175,55,0.42); border-radius:12px; padding:13px 16px; margin-bottom:12px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
        <div>
          <span class="kp-badge-pill kp-badge-gold">1. SIGNED CONTRACT PDF</span>
          <span style="font-size:0.8rem; color:#cbd5e1; margin-left:8px;">Base Contract: <strong style="color:#ffffff;">${fmtMoney(baseContract)}</strong> &bull; Signed with ${escapeHtml(t.contact)} (${escapeHtml(t.sub)})</span>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            📤 Upload Signed Contract PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleP4TradeContractUpload(${t.id}, event)" />
          </label>
        </div>
      </div>

      <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
          <div style="font-size:0.86rem; font-weight:800; color:#ffffff;">📄 ${escapeHtml(cPdf.name)}</div>
          <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
            Executed by Wayne Stevenson (#52603) &amp; ${escapeHtml(t.contact)} (${escapeHtml(t.sub)}) &bull; Date: ${escapeHtml(cPdf.date || t.startDate)}
          </div>
        </div>
        <div style="display:flex; gap:8px;">
          <button type="button" onclick="openTradeContractPdfOnScreen(${t.id})" class="kp-gold-btn kp-pill-sm">Open Contract PDF</button>
          <button type="button" onclick="downloadPartnerContractPdf(${t.id})" class="kp-secondary-btn kp-pill-sm">⬇️ Download PDF</button>
        </div>
      </div>
    </div>

    <!-- 2. CHANGE ORDERS (UPLOAD, ADD & DOWNLOAD) -->
    <div style="background:#080c14; border:1px solid rgba(212,175,55,0.42); border-radius:12px; padding:13px 16px; margin-bottom:12px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
        <div>
          <span class="kp-badge-pill kp-badge-gold">2. CHANGE ORDERS</span>
          <span style="font-size:0.8rem; color:#cbd5e1; margin-left:8px;">Total Change Orders: <strong style="color:#d4af37;">+${fmtMoney(coSum)}</strong> (${revs.length} Change Order${revs.length === 1 ? "" : "s"})</span>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="promptAddPartnerChangeOrder(${t.id})" class="kp-gold-btn kp-pill-sm">
            + Add Change Order
          </button>
          <label class="kp-secondary-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            📤 Upload Change Order PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleP4ChangeOrderPdfUpload(${t.id}, event)" />
          </label>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${revs.length === 0 ? `
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.1); border-radius:9px; padding:10px 14px; font-size:0.78rem; color:#94a3b8;">
            No Change Orders filed for ${escapeHtml(t.sub)}. Click "+ Add Change Order" or "Upload Change Order PDF" above if needed.
          </div>
        ` : revs.map(r => `
          <div style="background:#05070b; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
              <div style="font-size:0.86rem; font-weight:800; color:#ffffff;">
                <span style="color:#d4af37;">${escapeHtml(r.id)}</span> &mdash; ${escapeHtml(r.title)}
              </div>
              <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                Date: ${escapeHtml(r.date)} &bull; Cost Impact: <strong style="color:#d4af37;">+${fmtMoney(r.amount)}</strong> &bull; Days Added: <strong style="color:#ffffff;">+${Number(r.days) || 0} Days</strong> &bull; File: ${escapeHtml(r.pdfName)}
              </div>
            </div>
            <div style="display:flex; gap:8px;">
              <button type="button" onclick="openTradeRevisionPdfModal('${t.id}', '${escapeHtml(r.id)}')" class="kp-gold-btn kp-pill-sm">Open PDF</button>
              <button type="button" onclick="downloadTradeRevisionPdf('${t.id}', '${escapeHtml(r.id)}')" class="kp-secondary-btn kp-pill-sm">⬇️ Download PDF</button>
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- 3. NEW PLANS, DRAWINGS & SPECIFICATIONS (UPLOAD & DOWNLOAD) -->
    <div style="background:#080c14; border:1px solid rgba(212,175,55,0.42); border-radius:12px; padding:13px 16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
        <div>
          <span class="kp-badge-pill kp-badge-gold">3. PLANS, DRAWINGS &amp; REVISED SPECS</span>
          <span style="font-size:0.8rem; color:#cbd5e1; margin-left:8px;">Upload new plans, revised drawings, or shop specs &amp; download anytime</span>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <label class="kp-gold-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            📤 Upload New Plans / Drawing PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleUploadPartnerPlanPdf(${t.id}, event)" />
          </label>
          <button type="button" onclick="promptAddPartnerPlanEntry(${t.id})" class="kp-secondary-btn kp-pill-sm">
            + Add Plan / Drawing Set
          </button>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${plans.map(pl => `
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div>
              <div style="font-size:0.86rem; font-weight:800; color:#ffffff;">📐 ${escapeHtml(pl.title)}</div>
              <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                Revision: <strong style="color:#f3e5ab;">${escapeHtml(pl.rev || "Latest Set")}</strong> &bull; Date: ${escapeHtml(pl.date)} &bull; File: ${escapeHtml(pl.pdfName)}
              </div>
            </div>
            <div style="display:flex; gap:8px;">
              <button type="button" onclick="openPartnerPlanPdf(${t.id}, '${escapeHtml(pl.id)}')" class="kp-gold-btn kp-pill-sm">Open Plan PDF</button>
              <button type="button" onclick="downloadPartnerPlanPdf(${t.id}, '${escapeHtml(pl.id)}')" class="kp-secondary-btn kp-pill-sm">⬇️ Download Plan PDF</button>
            </div>
          </div>
        `).join("")}
      </div>
    </div>
  `;
};

// ============================================================================
// WHEN YOU CLICK ON BOX 3 (CITY INSPECTIONS, PERMITS & SCHEDULES):
// Opens the Master Page organized into 3 Clean Master Brackets:
//   - MASTER BRACKET 1: APPROVED PLANS & SCHEDULES (Schedule A, Schedule B, C-A, C-B)
//   - MASTER BRACKET 2: PERMITS MADE / PULLED (Building, Plumbing, Electrical, Mechanical, Civil)
//   - MASTER BRACKET 3: ALL INSPECTION REPORTS UNDERNEATH (Passed & Fix-Up Reports + Email to Trade)
// ============================================================================
function renderMasterCityPermitsAndInspectionsPage(job) {
  ensureArchitectToFinish22Trades(job);
  const detailView = document.getElementById("p4-trade-detail-view");
  if (!detailView) return;

  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const plans = cm.plansAndSchedules || [];
  const permits = cm.permitsMade || [];
  const reports = cm.inspectionReports || [];
  const muni = resolveJobMunicipality(job);

  detailView.innerHTML = `
    <!-- TOP BAR: BACK TO 3-BOX VIEW -->
    <div style="background:#080c14; border:1.5px solid #d4af37; border-radius:12px; padding:13px 16px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <button type="button" onclick="closeP4TradeDetailPage()" class="kp-gold-btn kp-pill-sm">
          &larr; Back to Consultants, Trades &amp; City Box
        </button>
        <span class="kp-badge-pill kp-badge-gold">MASTER CITY PERMITS, SCHEDULES &amp; INSPECTIONS</span>
        <h3 style="font-size:1.02rem; font-weight:900; color:#ffffff; margin:0;">
          ${escapeHtml(muni)} &mdash; Master Plans, Schedules (A / B / C-B), Permits &amp; Inspection Reports
        </h3>
      </div>
    </div>

    <!-- MASTER BRACKET 1: APPROVED PLANS & LETTERS OF ASSURANCE (SCHEDULE A / SCHEDULE B / C-A / C-B) -->
    <div style="background:#080c14; border:1.5px solid rgba(212,175,55,0.48); border-radius:12px; padding:14px 16px; margin-bottom:14px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <span class="kp-badge-pill kp-badge-gold">MASTER BRACKET 1 &bull; PLANS &amp; SCHEDULES (A / B / C-A / C-B)</span>
          <h4 style="font-size:0.96rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            Approved IFC Plans &amp; BC Building Code Letters of Assurance (Schedule A, Schedule B, Schedule C-A, Schedule C-B)
          </h4>
        </div>
        <button type="button" onclick="promptAddCityMasterItem('plan')" class="kp-gold-btn kp-pill-sm">
          + Upload / Add Schedule or Plan PDF
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${plans.map(item => `
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1;">
              <span class="kp-badge-pill kp-badge-gold" style="flex-shrink:0;">${escapeHtml(item.code)}</span>
              <div style="min-width:0; flex:1;">
                <div style="font-size:0.86rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(item.title)}</div>
                <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                  Professional / Firm: <strong style="color:#f3e5ab;">${escapeHtml(item.firm)}</strong> &bull; Date: ${escapeHtml(item.date)} &bull; File: ${escapeHtml(item.pdfName)}
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(item.status)}</span>
              <button type="button" onclick="openCityMasterPdf('plan', '${escapeHtml(item.id)}')" class="kp-gold-btn kp-pill-sm">Open PDF</button>
              <button type="button" onclick="downloadCityMasterPdf('plan', '${escapeHtml(item.id)}')" class="kp-secondary-btn kp-pill-sm">⬇️ Download</button>
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- MASTER BRACKET 2: PERMITS MADE / PULLED -->
    <div style="background:#080c14; border:1.5px solid rgba(212,175,55,0.48); border-radius:12px; padding:14px 16px; margin-bottom:14px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <span class="kp-badge-pill kp-badge-gold">MASTER BRACKET 2 &bull; PERMITS MADE &amp; PULLED</span>
          <h4 style="font-size:0.96rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            All Municipal &amp; Trade Permits Pulled for ${escapeHtml(job.address)}
          </h4>
        </div>
        <button type="button" onclick="promptAddCityMasterItem('permit')" class="kp-gold-btn kp-pill-sm">
          + Add / Upload Permit PDF
        </button>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${permits.map(prm => `
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1;">
              <span class="kp-badge-pill kp-badge-gold" style="flex-shrink:0;">${escapeHtml(prm.code)}</span>
              <div style="min-width:0; flex:1;">
                <div style="font-size:0.86rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHtml(prm.title)}</div>
                <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px;">
                  Authority: <strong style="color:#f3e5ab;">${escapeHtml(prm.authority)}</strong> &bull; Issued: ${escapeHtml(prm.date)} &bull; File: ${escapeHtml(prm.pdfName)}
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
              <span class="kp-badge-pill kp-badge-white">${escapeHtml(prm.status)}</span>
              <button type="button" onclick="openCityMasterPdf('permit', '${escapeHtml(prm.id)}')" class="kp-gold-btn kp-pill-sm">Open Permit PDF</button>
              <button type="button" onclick="downloadCityMasterPdf('permit', '${escapeHtml(prm.id)}')" class="kp-secondary-btn kp-pill-sm">⬇️ Download</button>
            </div>
          </div>
        `).join("")}
      </div>
    </div>

    <!-- MASTER BRACKET 3: ALL INSPECTION REPORTS UNDERNEATH -->
    <div style="background:#080c14; border:1.5px solid rgba(212,175,55,0.48); border-radius:12px; padding:14px 16px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <span class="kp-badge-pill kp-badge-gold">MASTER BRACKET 3 &bull; ALL INSPECTION REPORTS UNDERNEATH</span>
          <h4 style="font-size:0.96rem; font-weight:900; color:#ffffff; margin:4px 0 0 0;">
            All Municipal &amp; Engineering Inspection Reports (Passed &amp; Items to Fix Up — Auto-Syncs to Final Walkthrough Folder)
          </h4>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="promptAddCityMasterItem('report')" class="kp-gold-btn kp-pill-sm">
            + Add Inspection Report
          </button>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${reports.map(rpt => {
          const isPass = String(rpt.status).toUpperCase().includes("PASS");
          return `
            <div style="background:#05070b; border:1px solid ${isPass ? 'rgba(212,175,55,0.45)' : 'rgba(255,255,255,0.2)'}; border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
              <div style="min-width:0; flex:1;">
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                  <span class="kp-badge-pill ${isPass ? 'kp-badge-gold' : 'kp-badge-white'}">${escapeHtml(rpt.code)} &bull; ${escapeHtml(rpt.status)}</span>
                  <span style="font-size:0.86rem; font-weight:800; color:#ffffff;">${escapeHtml(rpt.title)}</span>
                </div>
                <div style="font-size:0.75rem; color:#f8fafc; margin-top:4px;">
                  ${escapeHtml(rpt.notes)}
                </div>
                <div style="font-size:0.71rem; color:#94a3b8; margin-top:3px;">
                  Trade / Consultant: <strong style="color:#f3e5ab;">${escapeHtml(rpt.trade)}</strong> &bull; Authority: ${escapeHtml(rpt.authority)} &bull; Date: ${escapeHtml(rpt.date)} &bull; 📍 ${escapeHtml(rpt.geotag)}
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:7px; flex-shrink:0;">
                <button type="button" onclick="toggleCityReportPassed('${escapeHtml(rpt.id)}')" class="${isPass ? 'kp-secondary-btn' : 'kp-gold-btn'} kp-pill-sm">
                  ${isPass ? 'Mark Needs Fix' : '✓ Mark Passed'}
                </button>
                <button type="button" onclick="emailCityInspectionReportToTrade('${escapeHtml(rpt.id)}')" class="kp-secondary-btn kp-pill-sm">
                  ✉️ Email Trade
                </button>
                <button type="button" onclick="openCityMasterPdf('report', '${escapeHtml(rpt.id)}')" class="kp-gold-btn kp-pill-sm">Open PDF</button>
                <button type="button" onclick="downloadCityMasterPdf('report', '${escapeHtml(rpt.id)}')" class="kp-secondary-btn kp-pill-sm">⬇️ Download</button>
              </div>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  `;
}

// Interactive helpers for Partner Page & Master City Page
function promptEditPartnerDetails(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const contact = prompt("Update Person We Are Working With:", t.contact || "");
  if (contact === null) return;
  const sub = prompt("Update Company / Firm Name:", t.sub || "");
  if (sub === null) return;
  const contract = prompt("Update Signed Contract Amount ($ CAD):", String(t.contract || 0));
  if (contract === null) return;
  const start = prompt("Update Start Date (YYYY-MM-DD):", t.startDate || "");
  if (start === null) return;
  const end = prompt("Update Finish Date (YYYY-MM-DD):", t.endDate || "");
  if (end === null) return;

  t.contact = contact.trim() || t.contact;
  t.sub = sub.trim() || t.sub;
  t.contract = Number(contract) || t.contract;
  t.startDate = start.trim() || t.startDate;
  t.endDate = end.trim() || t.endDate;
  saveState();
  renderAllPortalComponents();
  showToast("Updated " + t.name + " Details & Contract");
}

function downloadPartnerContractPdf(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const cPdf = t.contractPdf || { name: t.phase + "_Signed_Contract.pdf", date: t.startDate };
  const text = [
    "KEYSTONE POSSIBILITIES LTD. (#52603) — EXECUTED CONTRACT RECORD",
    "PROJECT: " + job.address,
    "SCOPE: " + t.phase + " — " + t.name,
    "WORKING WITH: " + t.contact + " (" + t.sub + ")",
    "SIGNED CONTRACT AMOUNT: " + fmtMoney(t.contract),
    "SCHEDULE: " + t.startDate + " to " + t.endDate
  ].join("\n");
  triggerDummyDownload(cPdf.name, text);
  showToast("⬇️ Downloaded " + cPdf.name);
}

function promptAddPartnerChangeOrder(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const title = prompt("Enter Change Order Description:", "Scope Addition / Plan Revision");
  if (!title) return;
  const amt = Number(prompt("Enter Change Order Amount ($ CAD):", "6500")) || 0;
  const days = Number(prompt("Enter Days Added to Schedule (0 if none):", "2")) || 0;
  const today = job.whereWeAreDate || "2026-10-24";

  t.revisions = t.revisions || [];
  const coId = "CO-" + t.phase + "-0" + (t.revisions.length + 1);
  t.revisions.push({
    id: coId,
    date: today,
    title: title.trim(),
    desc: title.trim(),
    amount: amt,
    days: days,
    pdfName: coId + "_" + String(t.sub || "Partner").replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 18) + ".pdf",
    signed: true,
    signedBy: job.ownerName || "Property Owner",
    signedDate: today
  });
  saveState();
  renderAllPortalComponents();
  showToast("Added Change Order " + coId + " (+" + fmtMoney(amt) + ")");
}

function downloadTradeRevisionPdf(tradeId, revId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => String(x.id) === String(tradeId));
  if (!t) return;
  const rev = (t.revisions || []).find(r => String(r.id) === String(revId));
  if (!rev) return;
  const text = [
    "KEYSTONE POSSIBILITIES LTD. (#52603) — CHANGE ORDER RECORD",
    "PROJECT: " + job.address,
    "CHANGE ORDER: " + rev.id + " — " + rev.title,
    "PARTNER: " + t.contact + " (" + t.sub + ")",
    "COST IMPACT: +" + fmtMoney(rev.amount) + " | SCHEDULE IMPACT: +" + (rev.days || 0) + " Days",
    "DATE: " + rev.date
  ].join("\n");
  triggerDummyDownload(rev.pdfName || (rev.id + ".pdf"), text);
  showToast("⬇️ Downloaded Change Order PDF: " + (rev.pdfName || rev.id));
}

function handleUploadPartnerPlanPdf(tradeId, ev) {
  const file = ev && ev.target && ev.target.files && ev.target.files[0];
  if (!file) return;
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const rev = prompt("Enter Revision / Plan Label (e.g. Rev 4 IFC Update):", "Revised Plan Set") || "Revised Plan Set";
  const reader = new FileReader();
  reader.onload = function(e) {
    t.partnerPlans = t.partnerPlans || [];
    t.partnerPlans.unshift({
      id: "PLN-" + t.phase + "-" + (t.partnerPlans.length + 1),
      title: file.name.replace(/\.[^/.]+$/, "").replace(/[_-]+/g, " "),
      rev: rev.trim(),
      date: job.whereWeAreDate || "2026-10-24",
      pdfName: file.name,
      dataUrl: e.target.result || ""
    });
    saveState();
    renderTradesList();
    showToast("Uploaded Plan PDF: " + file.name);
  };
  reader.readAsDataURL(file);
}

function promptAddPartnerPlanEntry(tradeId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const title = prompt("Enter Plan / Drawing Set Title:", "Updated Construction Drawing & Detail Sheet");
  if (!title) return;
  const rev = prompt("Enter Revision Label:", "Rev 4 — Issued for Construction") || "Latest Set";
  const today = job.whereWeAreDate || "2026-10-24";
  t.partnerPlans = t.partnerPlans || [];
  const fn = t.phase + "_" + title.trim().replace(/[^a-zA-Z0-9]+/g, "_").slice(0, 24) + ".pdf";
  t.partnerPlans.unshift({
    id: "PLN-" + t.phase + "-" + (t.partnerPlans.length + 1),
    title: title.trim(),
    rev: rev.trim(),
    date: today,
    pdfName: fn,
    dataUrl: ""
  });
  saveState();
  renderTradesList();
  showToast("Added Plan Set: " + title.trim());
}

function openPartnerPlanPdf(tradeId, planId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const pl = (t.partnerPlans || []).find(p => String(p.id) === String(planId));
  if (!pl) return;
  const body = [
    "PLANS, DRAWINGS & SPECIFICATION SET: " + pl.title,
    "PROJECT: " + job.address,
    "PARTNER: " + t.contact + " (" + t.sub + " • " + t.name + ")",
    "REVISION: " + pl.rev + " | DATE: " + pl.date,
    "FILE: " + pl.pdfName
  ].join("\n\n");
  openCustomVaultPdfOnScreen("Plan Set — " + pl.title, pl.pdfName, t.sub + " • " + pl.rev, body, pl.dataUrl || "");
}

function downloadPartnerPlanPdf(tradeId, planId) {
  const job = getActiveJob();
  const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
  if (!t) return;
  const pl = (t.partnerPlans || []).find(p => String(p.id) === String(planId));
  if (!pl) return;
  triggerDummyDownload(pl.pdfName, "KEYSTONE PLAN SET: " + pl.title + "\nPARTNER: " + t.sub + "\nREV: " + pl.rev + "\nDATE: " + pl.date);
  showToast("⬇️ Downloaded Plan PDF: " + pl.pdfName);
}

function promptAddCityMasterItem(kind) {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const cm = job.cityMasterVault;
  const today = job.whereWeAreDate || "2026-10-24";

  if (kind === "plan") {
    const code = prompt("Enter Schedule or Plan Code (e.g. SCHEDULE B, SCHEDULE C-B, IFC PLAN):", "SCHEDULE B");
    if (!code) return;
    const title = prompt("Enter Title:", "Assurance of Professional Field Review");
    if (!title) return;
    const firm = prompt("Enter Firm / Professional:", "Apex Structural P.Eng.") || "Registered Professional";
    const id = "SCH-" + (cm.plansAndSchedules.length + 1);
    cm.plansAndSchedules.unshift({
      id, code: code.trim().toUpperCase(), title: title.trim(), firm: firm.trim(),
      date: today, status: "SEALED & FILED", pdfName: job.jobId + "_" + code.trim().replace(/[^a-zA-Z0-9]+/g, "_") + ".pdf"
    });
  } else if (kind === "permit") {
    const code = prompt("Enter Permit #:", "PRM-2026-" + Math.floor(100 + Math.random() * 899));
    if (!code) return;
    const title = prompt("Enter Permit Description:", "Municipal Trade & Site Permit");
    if (!title) return;
    const id = "PRM-" + (cm.permitsMade.length + 1);
    cm.permitsMade.unshift({
      id, code: code.trim().toUpperCase(), title: title.trim(), authority: resolveJobMunicipality(job),
      date: today, status: "PERMIT ISSUED & ACTIVE", pdfName: job.jobId + "_" + code.trim().replace(/[^a-zA-Z0-9]+/g, "_") + ".pdf"
    });
  } else {
    const code = prompt("Enter Inspection Code (e.g. INSP-09 • ENVELOPE):", "INSP-0" + (cm.inspectionReports.length + 1));
    if (!code) return;
    const title = prompt("Enter Inspection Report Title:", "Municipal & Engineer Field Inspection Report");
    if (!title) return;
    const trade = prompt("Enter Trade / Consultant Involved:", "Pacific Ridge Timberworks") || "Site Trade";
    const notes = prompt("Enter Inspection Notes or Fix-Up Items:", "Passed field inspection; filed into walkthrough folder.") || "";
    const status = prompt("Status (PASSED or NEEDS FIX):", "PASSED") || "PASSED";
    const id = "RPT-" + (cm.inspectionReports.length + 1);
    cm.inspectionReports.unshift({
      id, code: code.trim().toUpperCase(), title: title.trim(), authority: resolveJobMunicipality(job) + " Inspector",
      trade: trade.trim(), date: today, geotag: getJobGeotagCoords(job), status: status.trim().toUpperCase(),
      notes: notes.trim(), pdfName: "Report_" + id + "_Inspection.pdf"
    });
  }
  saveState();
  renderAllPortalComponents();
  showToast("Added Record to Master City Permits, Schedules & Inspections Vault!");
}

function toggleCityReportPassed(rptId) {
  const job = getActiveJob();
  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const rpt = (cm.inspectionReports || []).find(r => String(r.id) === String(rptId));
  if (!rpt) return;
  const wasPass = String(rpt.status).toUpperCase().includes("PASS");
  rpt.status = wasPass ? "NEEDS FIX / ACTION" : "PASSED";
  saveState();
  renderAllPortalComponents();
  showToast(rpt.code + " updated to " + rpt.status);
}

function emailCityInspectionReportToTrade(rptId) {
  const job = getActiveJob();
  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const rpt = (cm.inspectionReports || []).find(r => String(r.id) === String(rptId));
  if (!rpt) return;
  const subject = `[Keystone Possibilities #52603] ${job.address} — ${rpt.code}: ${rpt.title}`;
  const body = [
    `Project: ${job.address} (${getCleanPropertyTypeLabel(job)})`,
    `Inspection / Report: ${rpt.code} — ${rpt.title}`,
    `Trade / Consultant: ${rpt.trade}`,
    `Status: ${rpt.status}`,
    `Authority: ${rpt.authority} | Date: ${rpt.date}`,
    `Geotag: ${rpt.geotag}`,
    ``,
    `Details / Required Action:`,
    rpt.notes,
    ``,
    `Wayne Stevenson — Keystone Possibilities Ltd. (BC Licensed Builder #52603)`
  ].join("\n");
  window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`, "_blank");
  showToast("✉️ Opened Email Dispatch for " + rpt.code);
}

function openCityMasterPdf(kind, itemId) {
  const job = getActiveJob();
  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const list = kind === "plan" ? cm.plansAndSchedules : (kind === "permit" ? cm.permitsMade : cm.inspectionReports);
  const item = (list || []).find(x => String(x.id) === String(itemId));
  if (!item) return;
  const body = [
    item.code + " — " + item.title,
    "PROJECT: " + job.address + " (" + getCleanPropertyTypeLabel(job) + ")",
    "AUTHORITY / FIRM: " + (item.firm || item.authority || ""),
    "STATUS: " + item.status + " | DATE: " + item.date,
    item.notes ? ("NOTES: " + item.notes) : "",
    "GEOTAG: " + getJobGeotagCoords(job)
  ].filter(Boolean).join("\n\n");
  openCustomVaultPdfOnScreen(item.code + " — " + item.title, item.pdfName, item.status + " • " + item.date, body, "");
}

function downloadCityMasterPdf(kind, itemId) {
  const job = getActiveJob();
  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const list = kind === "plan" ? cm.plansAndSchedules : (kind === "permit" ? cm.permitsMade : cm.inspectionReports);
  const item = (list || []).find(x => String(x.id) === String(itemId));
  if (!item) return;
  triggerDummyDownload(item.pdfName, item.code + " — " + item.title + "\nPROJECT: " + job.address + "\nSTATUS: " + item.status + "\nDATE: " + item.date);
  showToast("⬇️ Downloaded " + item.pdfName);
}

// ============================================================================
// 4. TAB 4: MASTER FINANCIALS & PDFS (Hide Waiver Bar)
// ============================================================================
const _origRenderTab6JobManager = renderTab6JobManager;
renderTab6JobManager = function() {
  _origRenderTab6JobManager();
  const hbBar = document.getElementById("p6-statutory-holdback-bar");
  if (hbBar) hbBar.style.setProperty("display", "none", "important");
  const hbBtn = document.getElementById("btn-p6-export-holdback-pdf");
  if (hbBtn) hbBtn.style.setProperty("display", "none", "important");
};

// ============================================================================
// 5. TAB 5: MATERIAL & FRAMING BREAKDOWN — SHIP ORDER TO DICK'S LUMBER / SUPPLIER
// ============================================================================
function shipMaterialTakeoffToSupplier(sectionTitle) {
  const job = getActiveJob();
  const supplier = prompt("Send Material Takeoff & Order List to Supplier (e.g. Dick's Lumber & Building Supplies):", "Dick's Lumber & Building Supplies (Squamish / Burnaby Commercial Desk)");
  if (!supplier) return;
  const body = [
    `To: ${supplier}`,
    `From: Wayne Stevenson — Keystone Possibilities Ltd. (BC Housing Builder #52603)`,
    `Job Site Delivery Address: ${job.address} (${getJobGeotagCoords(job)})`,
    `Permit #: ${job.permitNum || "BP2026-0419"}`,
    `Scope: ${sectionTitle || "Master Framing & Material Takeoff Package"}`
  ].join("\n");
  showToast(`🚚 Dispatched Material Takeoff Order (${sectionTitle || "Full Package"}) to ${supplier}!`);
  const fn = (job.jobId || "KP-2026-001") + "_" + String(sectionTitle || "Master_Materials").replace(/[^a-zA-Z0-9]+/g, "_") + "_Dicks_Lumber_Order.pdf";
  triggerDummyDownload(fn, body);
}

const _origRenderMaterialsList = renderMaterialsList;
renderMaterialsList = function() {
  _origRenderMaterialsList();
  const topBar = document.getElementById("p5-active-plans-small-bar");
  if (topBar && !document.getElementById("btn-ship-dicks-lumber")) {
    const btnWrap = topBar.querySelector("div:last-child");
    if (btnWrap) {
      const shipBtn = document.createElement("button");
      shipBtn.type = "button";
      shipBtn.id = "btn-ship-dicks-lumber";
      shipBtn.className = "kp-gold-btn kp-pill-sm";
      shipBtn.innerHTML = "🚚 Send Takeoff Order to Dick's Lumber / Supplier";
      shipBtn.onclick = () => shipMaterialTakeoffToSupplier("Master Framing & Lumber Takeoff");
      btnWrap.insertBefore(shipBtn, btnWrap.firstChild);
    }
  }
};

// ============================================================================
// 6. TAB 6: WBI NATIONAL HOME WARRANTY (ONE-TAP) + FINAL PASSED INSPECTIONS &
//    MASTER HANDOFF / WALKTHROUGH FOLDER
// ============================================================================
function downloadMasterFinalWalkthroughFolder() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const w = job.warranty || {};
  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const lines = [
    "============================================================================",
    "KEYSTONE POSSIBILITIES LTD. (BC HOUSING LICENSED BUILDER #52603)",
    "MASTER FINAL HANDOFF, WALKTHROUGH & WBI NATIONAL HOME WARRANTY FOLDER",
    "============================================================================",
    "PROJECT ADDRESS : " + job.address + " (" + getCleanPropertyTypeLabel(job) + ")",
    "PROPERTY OWNER  : " + (job.ownerName || "Property Owner"),
    "WARRANTY POLICY : WBI National Home Warranty (2-5-10 Year) — Policy #" + (w.policyNum || "WBI-2026-88421"),
    "MUNICIPAL PERMIT: #" + (job.permitNum || "BP2026-0419") + " (" + resolveJobMunicipality(job) + ")",
    "ON-SITE GEOTAG  : " + getJobGeotagCoords(job),
    "============================================================================",
    "",
    "PASSED CITY INSPECTIONS, PERMITS & SCHEDULE A/B/C-B SIGN-OFFS:"
  ];

  (cm.inspectionReports || []).forEach((rpt, i) => {
    lines.push(`${i + 1}. [${rpt.status}] ${rpt.code} — ${rpt.title} (${rpt.trade}) — Date: ${rpt.date}`);
  });

  const fn = (job.jobId || "KP-2026-001") + "_Master_Final_Walkthrough_And_WBI_Warranty_Folder.pdf";
  triggerDummyDownload(fn, lines.join("\n"));
  showToast("📦 Downloaded Complete Master Final Handoff & Walkthrough Folder!");
}

renderWarrantyAndPlansTab = function() {
  const job = getActiveJob();
  ensureArchitectToFinish22Trades(job);
  const w = job.warranty || {};
  w.provider = "WBI National Home Warranty";
  const geo = getJobGeotagCoords(job);
  const pane = document.getElementById("kp-page-3");
  if (!pane) return;

  const cm = job.cityMasterVault || buildMasterCityPermitsAndSchedulesVault(job);
  const passedReports = (cm.inspectionReports || []).filter(r => String(r.status).toUpperCase().includes("PASS"));
  const wbiPdfName = w.pdfName || (job.jobId + "_WBI_National_Home_Warranty_2_5_10_Certificate.pdf");

  pane.innerHTML = `
    <!-- BOX 1: WBI NATIONAL HOME WARRANTY (ONE-TAP UPLOAD / DOWNLOAD / OPEN) -->
    <div class="kp-card kp-exec-section" style="margin-bottom:1.1rem; border:1.5px solid #d4af37;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
            <span class="kp-badge-pill kp-badge-gold">WBI NATIONAL HOME WARRANTY &bull; ONE-TAP CERTIFICATE</span>
            <span class="kp-badge-pill kp-badge-white">BC LICENSED BUILDER #52603</span>
            <span class="kp-badge-pill kp-badge-white">POLICY #${escapeHtml(w.policyNum || "WBI-2026-88421")}</span>
          </div>
          <h2 class="kp-section-h2" style="font-size:1.16rem; margin:0;">
            WBI National Home Warranty (2-5-10 Year Home Warranty)
          </h2>
          <div style="font-size:0.78rem; color:#cbd5e1; margin-top:4px;">
            Click below to open the WBI National Home Warranty PDF on screen, download it, or upload an updated policy PDF.
          </div>
        </div>

        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="openWarrantyTierPdfOnScreen('master')" class="kp-gold-btn" style="padding:10px 18px !important; font-size:0.84rem !important;">
            📄 WBI National Home Warranty (One-Tap Open PDF)
          </button>
          <button type="button" onclick="downloadWarrantyCertificatePdf()" class="kp-secondary-btn kp-pill-sm">
            ⬇️ Download WBI Warranty PDF
          </button>
          <label class="kp-secondary-btn kp-pill-sm" style="cursor:pointer; margin:0;">
            📤 Upload WBI Warranty PDF
            <input type="file" accept=".pdf,image/*" style="display:none;" onchange="handleWarrantyPdfUpload(event)" />
          </label>
        </div>
      </div>

      <div onclick="openWarrantyTierPdfOnScreen('master')" style="margin-top:12px; background:#05070b; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; cursor:pointer;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="kp-badge-pill kp-badge-gold">WBI WARRANTY PDF</span>
          <div>
            <div style="font-size:0.86rem; font-weight:800; color:#ffffff;">${escapeHtml(wbiPdfName)}</div>
            <div style="font-size:0.72rem; color:#cbd5e1;">📍 ${escapeHtml(geo)} &bull; 2-Year Materials &amp; Labour &bull; 5-Year Building Envelope &bull; 10-Year Structural</div>
          </div>
        </div>
        <span style="font-size:0.78rem; font-weight:900; color:#d4af37;">Click to Open PDF &rarr;</span>
      </div>
    </div>

    <!-- BOX 2: FINAL PASSED INSPECTIONS & MASTER HANDOFF / WALKTHROUGH FOLDER -->
    <div class="kp-card kp-exec-section">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.1);">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="kp-badge-pill kp-badge-gold">FINAL PASSED INSPECTIONS &amp; MASTER WALKTHROUGH FOLDER</span>
            <span class="kp-badge-pill kp-badge-white">✓ ${passedReports.length} Passed Inspections Ready for Handoff</span>
          </div>
          <h2 class="kp-section-h2" style="font-size:1.06rem; margin-top:4px !important;">
            Master Final Handoff &amp; Walkthrough Folder (Download Individual Trade Inspections or Full Master Packet)
          </h2>
        </div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="downloadMasterFinalWalkthroughFolder()" class="kp-gold-btn kp-pill-sm">
            📦 Download Master Final Handoff &amp; Walkthrough Folder (${passedReports.length} Passed PDFs)
          </button>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:7px;">
        ${passedReports.map(rpt => `
          <div style="background:#060a12; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:9px 13px; display:flex; justify-content:space-between; align-items:center; flex-wrap:nowrap; gap:10px;">
            <div style="display:flex; align-items:center; gap:10px; min-width:0; flex:1;">
              <span class="kp-badge-pill kp-badge-gold" style="flex-shrink:0;">✓ PASSED &bull; ${escapeHtml(rpt.code)}</span>
              <div style="min-width:0; flex:1;">
                <div style="font-size:0.85rem; font-weight:800; color:#ffffff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                  ${escapeHtml(rpt.title)}
                </div>
                <div style="font-size:0.72rem; color:#cbd5e1; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                  Trade / Consultant: <strong style="color:#ffffff;">${escapeHtml(rpt.trade)}</strong> &bull; Authority: ${escapeHtml(rpt.authority)} &bull; Passed: ${escapeHtml(rpt.date)}
                </div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:7px; flex-shrink:0;">
              <button type="button" onclick="openCityMasterPdf('report', '${escapeHtml(rpt.id)}')" class="kp-secondary-btn kp-pill-sm">
                📄 Open PDF
              </button>
              <button type="button" onclick="downloadCityMasterPdf('report', '${escapeHtml(rpt.id)}')" class="kp-gold-btn kp-pill-sm">
                ⬇️ Download Inspection
              </button>
            </div>
          </div>
        `).join("")}
      </div>
    </div>
  `;
};

try {
  renderJobSelectors();
  renderAllPortalComponents();
} catch (e) {
  console.warn("v13 init render warning:", e);
}


// ============================================================================
// KEYSTONE PORTAL v14.0 — SINGLE ACTIVE JOB LOCK (40484 Tantalus Rd, Squamish)
// + PAGE 1 CANONICAL LOGIN GATE STYLING (Black Pill + White Text + Gold Hover Wave)
// ============================================================================
(function() {
  function injectLoginGateCanonicalStyles() {
    /* Canonical login gate styles served via assets/css/portal-v10.css */
    return;
  }

  function enforceSingleTantalusJobOnly() {
    if (typeof portalStore !== "undefined" && portalStore && Array.isArray(portalStore.jobs)) {
      const tantalus = portalStore.jobs.find(j => j.jobId === "KP-2026-001") || portalStore.jobs[0];
      if (tantalus) {
        tantalus.jobId = "KP-2026-001";
        tantalus.address = "40484 Tantalus Rd, Squamish, BC";
        portalStore.jobs = [tantalus];
        portalStore.activeJobId = "KP-2026-001";
      }
    }
    const loginSel = document.getElementById("ks-job-select");
    if (loginSel) {
      loginSel.innerHTML = `<option value="KP-2026-001" selected>40484 Tantalus Rd, Squamish, BC (KP-2026-001)</option>`;
    }
    const clientInput = document.getElementById("ks-client-id");
    if (clientInput) {
      clientInput.value = "40484 Tantalus Rd, Squamish, BC";
    }
  }

  injectLoginGateCanonicalStyles();
  enforceSingleTantalusJobOnly();

  const _prevRenderJobSelectors = typeof renderJobSelectors === "function" ? renderJobSelectors : null;
  renderJobSelectors = function() {
    enforceSingleTantalusJobOnly();
    const hdrSel = document.getElementById("kp-header-job-select");
    if (hdrSel) hdrSel.style.setProperty("display", "none", "important");
    const activeJob = typeof getActiveJob === "function" ? getActiveJob() : null;
    const staticTitle = document.getElementById("kp-header-static-job-title");
    if (staticTitle && activeJob) staticTitle.innerText = activeJob.address;
    const staticSub = document.getElementById("kp-header-static-job-sub");
    if (staticSub && activeJob && typeof getCleanPropertyTypeLabel === "function") {
      staticSub.innerText = getCleanPropertyTypeLabel(activeJob);
    }
  };

  // Override daemon sync so it never re-adds KP-2026-002..005 into portalStore.jobs
  const _prevSyncDaemon = typeof syncPortalFromDaemonV10Jobs === "function" ? syncPortalFromDaemonV10Jobs : null;
  syncPortalFromDaemonV10Jobs = async function(silent) {
    enforceSingleTantalusJobOnly();
  };

  try {
    localStorage.removeItem("KEYSTONE_PORTAL_V10_MULTI_JOB_STORE");
    localStorage.removeItem("KEYSTONE_PORTAL_V13_3BOX_MASTER");
    enforceSingleTantalusJobOnly();
    saveState(true);
  } catch (e) {}
})();


// ============================================================================
// KEYSTONE PORTAL v15.0 — PAGE 1 CANONICAL VISUAL STANDARD ACROSS ALL 6 TABS,
// ZERO CHANGE ORDERS / ZERO EXTRA FEES / 0 DAYS OVER,
// "HOW WE WANT IT BUILT" BCBC 2024 EXECUTION CHECKLIST FOR ALL 30 PARTNERS,
// & 5-DROP DICK'S LUMBER (#52603-KEYSTONE) MATERIAL TAKEOFF LISTS OFF PLANS
// ============================================================================
(function() {
  function injectPortalV15CanonicalStyles() {
    /* Canonical v15 portal styles served via assets/css/portal-v10.css */
    return;
  }

  function injectTopHeroBannerIntoPortal() {
    const mainEl = document.querySelector("#ks-authenticated-portal main.kp-portal-main");
    const navEl = document.getElementById("kp-master-nav");
    if (!mainEl || !navEl) return;
    if (document.getElementById("kp-v15-top-hero-banner")) return;

    const banner = document.createElement("div");
    banner.id = "kp-v15-top-hero-banner";
    banner.innerHTML = `
      <div>
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
          <span class="kp-badge-pill kp-badge-gold">ACTIVE PROJECT &bull; KP-2026-001</span>
          <span class="kp-badge-pill kp-badge-white">BC HOUSING LICENSED BUILDER #52603</span>
          <span class="kp-badge-pill kp-badge-white">0 CHANGE ORDERS ($0.00 CAD) &bull; 0 DAYS OVER</span>
        </div>
        <h1 class="kp-portal-hero-h1">
          <span class="kp-portal-h1-white" id="kp-v15-hero-addr">40484 Tantalus Rd, Squamish, BC</span>
          <span class="kp-portal-h1-gold">Open-Book CCDC 5B Client, Consultant &amp; Trade Command</span>
        </h1>
      </div>
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <div style="background:#060a12; border:1px solid rgba(212,175,55,0.48); border-radius:12px; padding:8px 14px; text-align:right;">
          <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase; letter-spacing:0.06em;">Baseline Contract &amp; Change Orders</div>
          <div style="font-size:0.98rem; font-weight:900; color:#ffffff;">$1,850,000 CAD <span style="color:#d4af37; font-size:0.82rem;">(+$0.00 Change Orders)</span></div>
        </div>
      </div>
    `;
    mainEl.insertBefore(banner, navEl);
  }

  function purgeDefaultSampleRevisionsEverywhere() {
    if (typeof portalStore !== "undefined" && portalStore && Array.isArray(portalStore.jobs)) {
      portalStore.jobs.forEach(job => {
        if (Array.isArray(job.trades)) {
          job.trades.forEach(tr => {
            if (Array.isArray(tr.revisions)) {
              tr.revisions = tr.revisions.filter(r => r && r.id !== "CO-001" && r.id !== "CO-002");
            }
          });
        }
      });
    }
  }

  // Build tailored "How We Want It Built — BCBC 2024 Execution & Quality Checklist" for each Consultant/Trade
  window.getPartnerHowWeWantItBuiltSpecs = function(t) {
    const ph = String(t.phase || "").toUpperCase();
    const nm = String(t.name || "").toLowerCase();
    const isCons = t.category === "consultant" || ph.startsWith("C-");

    if (isCons) {
      return {
        codeRef: "BC Building Code 2024 Div. C Part 2 & Letters of Assurance (Schedules A, B, C-A, C-B)",
        customHomeStd: "Full IFC sealed drawings coordinated with architectural, structural, geotech, and Step Code 4 mechanical/envelope before mobilization; mandatory field review report uploaded within 48 hours of site inspection.",
        multiplexStd: "4-Unit Bill 44 SSMUH compliance: verified fire separation ratings (1-hr/2-hr), STC 55+ acoustic party wall assemblies, BC Hydro ES54 400A multi-meter layout, and individual unit HRV balance schedules.",
        holdPoints: [
          "100% digital PDF drawing & schedule coordination across all 6 disciplines prior to permit or construction.",
          "Zero unapproved field substitutions — any site modification requires written P.Eng. / Architect Field Instruction.",
          "Signed Schedule B before start of discipline work and Schedule C-B prior to Municipal Final Occupancy."
        ]
      };
    }

    if (ph === "T-01" || ph === "T-02" || ph === "T-03" || nm.includes("excavat") || nm.includes("blast") || nm.includes("site")) {
      return {
        codeRef: "BCBC 2024 Part 4 / Part 9.12 Excavation, Shoring & Thurber Geotech 300 kPa Bearing Standard",
        customHomeStd: "Install high-visibility SPEA tree protection fencing and perimeter silt traps prior to machine entry. Strip all organic overburden down to competent granodiorite bedrock or undisturbed glacial till verified at 300 kPa by Geotechnical P.Eng.",
        multiplexStd: "Full footprint benching and rock-bolt stabilization for multi-unit foundation steps; coordinate deep utility trenching for 4-unit sanitary, storm retention chamber, and BC Hydro ES54 primary duct bank.",
        holdPoints: [
          "BCLS corner offset pins and elevation benchmark verified before bulk cut.",
          "Geotechnical P.Eng. subgrade bearing memo signed and uploaded to Portal before footing formwork begins.",
          "3/4\" clear crushed rock drainage blanket compacted in 150mm lifts with zero organic fines."
        ]
      };
    }

    if (ph === "T-05" || ph === "T-06" || ph === "T-07" || ph === "T-08" || nm.includes("concrete") || nm.includes("form") || nm.includes("waterproof")) {
      return {
        codeRef: "BCBC 2024 9.13 Hydrostatic Waterproofing, 9.14 Perimeter Drainage & 9.13.4 Active Radon Mitigation",
        customHomeStd: "32–35 MPa CSA A23.1 concrete with 15M/20M seismic rebar per S-102. Dual-layer elastomeric waterproofing + high-density dimple drainage matrix + dual rigid PVC 4\" weeping & rain-leader lines on washed drain rock. 100mm washed gas-permeable radon rock layer + 15-mil Stego vapour retarder + active sub-slab radon exhaust stack.",
        multiplexStd: "Continuous seismic grade beams and thickened slab-on-grade zones for multi-unit shear loads; dedicated sub-slab radon collector branches and acoustic slab isolation joints between lower-level suites.",
        holdPoints: [
          "Apex Structural P.Eng. Schedule B rebar & Simpson PAB/HDU anchor bolt inspection PASSED prior to pour.",
          "Hydrostatic membrane termination bar, filter cloth wrap, and weeping tile slope verified before backfill.",
          "10-foot head test on underslab DWV plumbing and sealed radon pipe penetration check prior to slab placement."
        ]
      };
    }

    if (ph === "T-09" || ph === "T-10" || ph === "T-11" || nm.includes("fram") || nm.includes("steel") || nm.includes("window")) {
      return {
        codeRef: "BCBC 2024 Part 4 Seismic Shear Walls, Simpson Strong-Tie ATS/HDU Schedule & Step Code 4 Fenestration",
        customHomeStd: "Kiln-dried #2 & Better D-Fir/Hem-Fir 2x6 exterior walls @ 16\" O.C., engineered TJI floor joists glued & ring-shank nailed with 3/4\" T&G OSB subfloor, and full Simpson HDU8/MSTC strap installation per S-101. Triple-glazed Low-E Argon windows flashed with sloped sill pans and liquid-applied jamb membranes.",
        multiplexStd: "Double-stud or staggered 2x4 acoustic party walls with 25mm air gap and fire-stopped floor/ceiling intersections between all 4 Bill 44 units; continuous multi-storey ATS tie-down rods torqued and inspected at every floor lift.",
        holdPoints: [
          "Moisture content of framing lumber verified <= 19% prior to enclosure and insulation.",
          "100% of shear wall ply edge nailing (3\" O.C.) and hold-down bolts inspected by Structural P.Eng. before exterior wrap.",
          "Window rough-opening sill slope and liquid/peel-and-stick flashing sequence photo-documented."
        ]
      };
    }

    if (ph === "T-12" || ph === "T-13" || nm.includes("roof") || nm.includes("siding") || nm.includes("envelope")) {
      return {
        codeRef: "BCBC 2024 9.27 Coastal Rainscreen Capillary Break & BC Energy Step Code 4 Envelope Continuity",
        customHomeStd: "High-temp self-adhered ice & water membrane across full low-slope/eave zones + Architectural standing-seam metal / heavy shingle system. Exterior 60mm continuous rigid stone-wool insulation over spun-bonded weather barrier + 19mm treated rainscreen strapping creating a positive drained & ventilated cavity + bug screen at base/top.",
        multiplexStd: "Non-combustible fibre-cement / architectural metal cladding on spatial separation faces; fire-stopped rainscreen cavity baffles at inter-unit floor lines and party wall intersections.",
        holdPoints: [
          "Blower-door mid-construction air barrier test verified <= 1.0 ACH50 before drywall.",
          "Building Envelope P.Eng. field review of through-wall flashings, saddle flashings, and deck ledger waterproofing.",
          "Zero unsealed penetrations through exterior air/vapour barrier."
        ]
      };
    }

    if (ph === "T-14" || ph === "T-15" || ph === "T-16" || ph === "T-17" || nm.includes("plumb") || nm.includes("hvac") || nm.includes("electr") || nm.includes("sprinkler")) {
      return {
        codeRef: "BCBC 2024 Part 6 / 9.32 Mechanical HRV, NFPA 13D Fire Suppression & Canadian Electrical Code 400A/EVEMS",
        customHomeStd: "PEX-a manifold domestic water with insulated hot water recirculation, cast-iron quiet vertical waste stacks, cold-climate variable-capacity heat pump + dedicated Zehnder HRV balanced ventilation, and 200A/400A service with Level 2 EV charger rough-ins.",
        multiplexStd: "Individual sub-metered 400A multi-gang switchgear with EVEMS load management per unit, independent unit HRV & heat pump zones (zero cross-unit air recirculation), and fire/acoustic putty pads on all electrical boxes in party walls.",
        holdPoints: [
          "All DWV, domestic water (100 PSI), hydronic loops, and NFPA 13D fire sprinkler lines pressure-tested and signed off.",
          "Zero structural joist or LVL beam web penetrations outside engineered allowable zones on S-101.",
          "TECA ventilation balancing report and Technical Safety BC electrical rough-in & final approvals uploaded."
        ]
      };
    }

    return {
      codeRef: "BC Building Code 2024 Part 9 & Keystone Possibilities #52603 Sovereign Quality Standard",
      customHomeStd: "Execute all work strictly to IFC Architectural & Interior Design drawings (A-101..A-107). Maintain laser-level tolerances, dust-extracted site cleanliness, and full protection of installed hardwood, glazing, and millwork surfaces.",
      multiplexStd: "Maintain STC 55+ acoustic integrity and 1-hr/2-hr fire-resistance ratings at all inter-dwelling walls, ceilings, penetrations, and suite entry doors across all units.",
      holdPoints: [
        "Pre-installation substrate & moisture verification completed with Site Superintendent Wayne Stevenson.",
        "All trade-specific inspection sign-offs and product warranty certificates uploaded to the Portal before progress draw release.",
        "Zero-deficiency walkthrough sign-off prior to 10% Statutory Builders Lien Holdback release."
      ]
    };
  };

  window.openPartnerHowWeWantItBuiltPdf = function(tradeId) {
    const job = getActiveJob();
    ensureArchitectToFinish22Trades(job);
    const t = (job.trades || []).find(x => Number(x.id) === Number(tradeId));
    if (!t) return;
    const spec = window.getPartnerHowWeWantItBuiltSpecs(t);
    const body = [
      `KEYSTONE POSSIBILITIES LTD. (BC HOUSING LICENSED BUILDER #52603)`,
      `"HOW WE WANT IT BUILT" — BCBC 2024 EXECUTION & INSPECTION CHECKLIST`,
      `========================================================================`,
      `PROJECT: ${job.address} (${job.jobId}) | PERMIT: #${job.permitNum || "BP2026-0419"}`,
      `PARTNER: ${t.phase} — ${t.name} (${t.sub})`,
      `PRIMARY CONTACT: ${t.contact} | ${t.phone || "(604) 848-9688"} | ${t.email}`,
      `CODE & ENGINEERING STANDARD: ${spec.codeRef}`,
      ``,
      `1. SINGLE-FAMILY LUXURY CUSTOM HOME EXECUTION STANDARD:`,
      `${spec.customHomeStd}`,
      ``,
      `2. 4-UNIT BILL 44 MULTIPLEX / MULTI-FAMILY EXECUTION STANDARD:`,
      `${spec.multiplexStd}`,
      ``,
      `3. MANDATORY QUALITY HOLD POINTS & INSPECTION SIGN-OFFS:`,
      ...spec.holdPoints.map((hp, i) => `   [✓] Hold Point ${i + 1}: ${hp}`),
      ``,
      `4. OPEN-BOOK CCDC 5B & 10% BUILDERS LIEN ACT HOLDBACK TERMS:`,
      `   - Base Signed Contract: ${fmtMoney(Number(t.contract) || 0)}`,
      `   - Approved Change Orders: $0.00 CAD (0 Days Over)`,
      `   - 10% Statutory Builders Lien Holdback Retained: ${fmtMoney(Math.round((Number(t.contract) || 0) * 0.10))}`,
      `   - 90% Net Progress Payable Upon Verified Inspection Sign-Off: ${fmtMoney((Number(t.contract) || 0) - Math.round((Number(t.contract) || 0) * 0.10))}`
    ].join("\n");
    openCustomVaultPdfOnScreen(
      `${t.phase} — How We Want It Built (BCBC 2024 Execution Standard)`,
      `${job.jobId}_${t.phase}_How_We_Want_It_Built_Checklist.pdf`,
      `${t.name} • ${t.sub} • BC Licensed Builder #52603`,
      body,
      ""
    );
  };

  // Override renderSelectedTrade3SectionPage to include 10% Holdback, $0.00 Change Orders / 0 Days Over, and Bracket 4 ("How We Want It Built")
  const _v13RenderSelectedTrade = renderSelectedTrade3SectionPage;
  renderSelectedTrade3SectionPage = function(job, t) {
    _v13RenderSelectedTrade(job, t);
    const detailView = document.getElementById("p4-trade-detail-view");
    if (!detailView || !t) return;

    const baseContract = Number(t.contract) || 0;
    const revs = (t.revisions || []).filter(Boolean);
    const coSum = revs.filter(r => r.signed).reduce((s, r) => s + (Number(r.amount) || 0), 0);
    const daysOver = revs.filter(r => r.signed).reduce((s, r) => s + (Number(r.daysImpact) || 0), 0);
    const totalContract = baseContract + coSum;
    const holdback10 = Math.round(totalContract * 0.10);
    const net90 = totalContract - holdback10;
    const spec = window.getPartnerHowWeWantItBuiltSpecs(t);

    if (!document.getElementById("kp-v15-how-we-want-it-built-box")) {
      const box = document.createElement("div");
      box.id = "kp-v15-how-we-want-it-built-box";
      box.style.cssText = "background:#080c14; border:1.5px solid rgba(212,175,55,0.58); border-radius:12px; padding:15px 18px; margin-top:12px;";
      box.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.12);">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
              <span class="kp-badge-pill kp-badge-gold">4. HOW WE WANT IT BUILT &bull; BCBC 2024 EXECUTION CHECKLIST</span>
              <span class="kp-badge-pill kp-badge-white">CUSTOM HOME &amp; BILL 44 MULTIPLEX STANDARD</span>
              <span class="kp-badge-pill kp-badge-white">CHANGE ORDERS: ${fmtMoney(coSum)} &bull; EXTRA FEES: $0.00 &bull; ${daysOver} DAYS OVER</span>
            </div>
            <h3 style="font-size:1.02rem; font-weight:800; color:#ffffff; margin:0;">
              ${escapeHtml(t.phase)} &mdash; ${escapeHtml(t.name)} Execution Standard &amp; 10% Lien Holdback Breakdown
            </h3>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button type="button" onclick="openPartnerHowWeWantItBuiltPdf(${t.id})" class="kp-gold-btn kp-pill-sm">
              📄 Open / Print "How We Want It Built" Spec PDF
            </button>
          </div>
        </div>

        <!-- 4-Card Partner Financial & Holdback Bar -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:12px;">
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:9px 12px;">
            <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase;">Base Signed Contract</div>
            <div style="font-size:1.02rem; font-weight:900; color:#ffffff; margin-top:2px;">${fmtMoney(baseContract)}</div>
          </div>
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:9px 12px;">
            <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase;">Change Orders &amp; Extra Fees</div>
            <div style="font-size:1.02rem; font-weight:900; color:#ffffff; margin-top:2px;">${fmtMoney(coSum)} <span style="font-size:0.75rem; color:#d4af37;">(${daysOver} Days Over)</span></div>
          </div>
          <div style="background:#05070b; border:1px solid rgba(212,175,55,0.48); border-radius:10px; padding:9px 12px;">
            <div style="font-size:0.65rem; font-weight:800; color:#f3e5ab; text-transform:uppercase;">10% Builders Lien Holdback</div>
            <div style="font-size:1.02rem; font-weight:900; color:#d4af37; margin-top:2px;">${fmtMoney(holdback10)}</div>
          </div>
          <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:9px 12px;">
            <div style="font-size:0.65rem; font-weight:800; color:#cbd5e1; text-transform:uppercase;">90% Net Progress Payable</div>
            <div style="font-size:1.02rem; font-weight:900; color:#ffffff; margin-top:2px;">${fmtMoney(net90)}</div>
          </div>
        </div>

        <!-- Custom Home vs Multiplex Execution Grid -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:10px; margin-bottom:10px;">
          <div style="background:#05070b; border:1px solid rgba(212,175,55,0.35); border-radius:10px; padding:11px 14px;">
            <div style="font-size:0.72rem; font-weight:800; color:#d4af37; text-transform:uppercase; margin-bottom:4px;">
              🏛️ Luxury Single-Family Custom Home Standard
            </div>
            <div style="font-size:0.84rem; color:#ffffff; line-height:1.5;">
              ${escapeHtml(spec.customHomeStd)}
            </div>
          </div>
          <div style="background:#05070b; border:1px solid rgba(212,175,55,0.35); border-radius:10px; padding:11px 14px;">
            <div style="font-size:0.72rem; font-weight:800; color:#d4af37; text-transform:uppercase; margin-bottom:4px;">
              🏢 4-Unit Bill 44 Multiplex / Multi-Family Standard
            </div>
            <div style="font-size:0.84rem; color:#ffffff; line-height:1.5;">
              ${escapeHtml(spec.multiplexStd)}
            </div>
          </div>
        </div>

        <!-- Mandatory Quality Hold Points -->
        <div style="background:#05070b; border:1px solid rgba(255,255,255,0.14); border-radius:10px; padding:11px 14px;">
          <div style="font-size:0.72rem; font-weight:800; color:#ffffff; text-transform:uppercase; margin-bottom:6px;">
            ✓ Mandatory BCBC 2024 Hold Points (${escapeHtml(spec.codeRef)})
          </div>
          <div style="display:flex; flex-direction:column; gap:5px;">
            ${spec.holdPoints.map((hp, idx) => `
              <div style="font-size:0.82rem; color:#e2e8f0; display:flex; align-items:flex-start; gap:8px;">
                <span style="color:#d4af37; font-weight:900;">[${idx + 1}]</span>
                <span>${escapeHtml(hp)}</span>
              </div>
            `).join("")}
          </div>
        </div>
      `;
      detailView.appendChild(box);
    }
  };

  // ============================================================================
  // TAB 5: 5-DROP PRINTABLE DICK'S LUMBER MATERIAL TAKEOFF LISTS OFF THE 13 PLANS
  // ============================================================================
  window.KP_DICKS_LUMBER_5_DROPS = [
    {
      dropNum: 1,
      id: "DROP-01",
      title: "Drop 1 — Foundation Formwork, PWF Sill Plates & 3/4\" Subfloor Package",
      sheets: "Extracted from Sheets A-101, S-101 & S-102",
      deliveryStage: "Stage 05–08 (Foundation & Subfloor Deck)",
      supplier: "Dick's Lumber & Building Supplies — Account #52603-KEYSTONE",
      items: [
        "42 pcs — 2x6x16' CSA Pressure-Treated Hem-Fir Mudsills (Incised, Above/Ground Contact)",
        "6 rolls — Frost King / Owens Corning 5-1/2\" Sill Plate Foam Gasket Seal",
        "118 sheets — 4'x8'x3/4\" (19mm) Select T&G Edge-Gold Structural OSB Subfloor Sheathing",
        "96 tubes — LePage PL Premium Max Heavy-Duty Subfloor Construction Adhesive (825 mL)",
        "48 pcs — 2x10x16' #2 & Btr D-Fir Formwork Walers, Bracing & Rim Blocking",
        "85 lengths — 15M & 20M Grade 400W Deformed Reinforcing Rebar + Pre-Bent 90° Corner Stirrups",
        "64 pcs — Simpson Strong-Tie PAB8-24 / SSTB24 Anchor Bolts & HDG Washer Plates"
      ]
    },
    {
      dropNum: 2,
      id: "DROP-02",
      title: "Drop 2 — Main & Upper 2x6 Kiln-Dried Wall Framing, TJI Joists & Parallam LVL Beams",
      sheets: "Extracted from Sheets A-102, A-103 & S-101",
      deliveryStage: "Stage 09–10 (Primary Structural Wood Framing)",
      supplier: "Dick's Lumber & Building Supplies — Account #52603-KEYSTONE",
      items: [
        "640 pcs — 2x6x104-5/8\" Precision End-Trimmed KD #2 & Btr SPF/Hem-Fir Exterior Wall Studs",
        "480 pcs — 2x4x104-5/8\" KD SPF Interior Partition & Acoustic Staggered Party-Wall Studs",
        "110 pcs — 2x6x16' KD #2 & Btr Double Top Plates & Bottom Wall Plates",
        "68 lengths — 11-7/8\" TJI 360 Engineered Wood I-Joists (24'–32' Cut-to-Span Package per S-101)",
        "14 pcs — 1-3/4\" x 11-7/8\" x 20' Microllam LVL Rim Board & Stairwell Header Stock",
        "6 pcs — 5-1/4\" x 14\" Parallam PSL Structural Flush-Frame Ridge & Garage Header Beams",
        "145 sheets — 4'x8'x1/2\" (12.5mm) D-Fir Structural 1 Rated Shear Wall Plywood"
      ]
    },
    {
      dropNum: 3,
      id: "DROP-03",
      title: "Drop 3 — Engineered Roof Trusses, 5/8\" D-Fir Roof Decking & High-Temp Underlayment",
      sheets: "Extracted from Sheets A-104 & S-101",
      deliveryStage: "Stage 10–12 (Roof Structure & Dry-In)",
      supplier: "Dick's Lumber & Building Supplies — Account #52603-KEYSTONE",
      items: [
        "1 Lot (34 Trusses) — Engineered Snow-Load Roof Truss Package (Squamish 3.4 kPa Ground Snow Load Sealed)",
        "92 sheets — 4'x8'x5/8\" (15.5mm) D-Fir T&G Structural Roof Deck Sheathing",
        "180 pcs — 2x4x16' KD SPF Truss Lateral Web Bracing & Soffit Lookouts",
        "32 pcs — 2x8x16' Select Str. Fascia & Barge Sub-Fascia Stock",
        "14 rolls — Grace Ice & Water Shield HT Self-Adhered High-Temp Roof Membrane",
        "8 boxes — Simpson Strong-Tie H2.5A / H10A Stainless/Galvanized Hurricane Truss Ties"
      ]
    },
    {
      dropNum: 4,
      id: "DROP-04",
      title: "Drop 4 — Seismic Hold-Downs, Simpson Strong-Tie ATS Rods & Structural Hardware",
      sheets: "Extracted from Sheets S-101 & S-102",
      deliveryStage: "Stage 10 (Seismic Shear Wall & Tie-Down Inspection)",
      supplier: "Dick's Lumber & Building Supplies — Account #52603-KEYSTONE",
      items: [
        "24 sets — Simpson Strong-Tie HDU8-SDS2.5 Pre-Deflected Hold-Downs with 3/4\" Anchor Rods",
        "16 sets — Simpson Strong-Tie ATS Continuous Multi-Storey Rod Tie-Down System + Take-Up Devices",
        "36 pcs — Simpson Strong-Tie MSTC40 / LSTA24 Floor-to-Floor Tension Straps",
        "72 pcs — Simpson Strong-Tie IUS2.56/11.88 Face-Mount I-Joist Hangers & LUS210 Beam Hangers",
        "18 buckets — Simpson Strong-Tie SDS Heavy-Duty 1/4\"x3-1/2\" Structural Connector Screws",
        "24 cases — Paslode / Bostitch 2-3/8\" x 0.113\" Hot-Dipped Galvanized Ring-Shank Shear Wall Nails (3\" O.C. Grid)"
      ]
    },
    {
      dropNum: 5,
      id: "DROP-05",
      title: "Drop 5 — BCBC 9.27 Rainscreen Strapping, 60mm Exterior Rockwool & Step Code 4 Airtight Package",
      sheets: "Extracted from Sheets A-105, A-106 & A-107",
      deliveryStage: "Stage 12–13 (Building Envelope & Step Code 4 Air Barrier)",
      supplier: "Dick's Lumber & Building Supplies — Account #52603-KEYSTONE",
      items: [
        "16 rolls — Siga Majvest / DuPont Tyvek DrainWrap Vapour-Permeable Air/Weather Barrier",
        "84 bundles — Rockwool Comfortboard 80 (60mm / 2.36\" Rigid Exterior Continuous Stone-Wool Insulation)",
        "310 pcs — 1x4x12' (19x89mm) CSA Pressure-Treated Plywood/Fir Vertical Rainscreen Furring Straps",
        "28 rolls — Siga Wigluv / 3M 8067 All-Weather Exterior Air-Barrier & Window Flashing Tape",
        "18 rolls — Cor-A-Vent SV-3 / Stainless Mesh Continuous Top & Bottom Rainscreen Insect/Vent Strip",
        "12 buckets — 5\" Structural Exterior Insulation Fastening Screws with 2\" Thermal Washers"
      ]
    }
  ];

  window.openDicksLumberDropPdf = function(dropNum) {
    const job = getActiveJob();
    const allDrops = window.KP_DICKS_LUMBER_5_DROPS || [];
    if (dropNum === "ALL" || dropNum === 0) {
      const masterLines = [
        `KEYSTONE POSSIBILITIES LTD. (BC HOUSING LICENSED BUILDER #52603)`,
        `DICK'S LUMBER COMMERCIAL DESK — MASTER 5-DROP TAKEOFF ORDER LIST (DROPS #1–#5)`,
        `========================================================================`,
        `SUPPLIER ACCOUNT : Dick's Lumber & Building Supplies — Account #52603-KEYSTONE`,
        `DELIVERY SITE    : ${job.address} (${job.jobId}) | Permit #${job.permitNum || "BP2026-0419"}`,
        `SUPERINTENDENT   : Wayne Stevenson — (604) 848-9688`,
        `BLUEPRINT SHEETS : All 13 IFC Sheets (A-101..A-302, S-101..S-103, C-101, G-101, M-101, E-101, EN-101)`,
        `TOTAL DROPS      : 5 Staged Crane/Moffett Delivery Packages (38 Line Items Total)`,
        `========================================================================`
      ];
      allDrops.forEach(d => {
        masterLines.push(
          ``,
          `[${d.id}] ${d.title}`,
          `Sheets: ${d.sheets} | Delivery Window: ${d.deliveryStage}`,
          `------------------------------------------------------------------------`,
          ...d.items.map((item, idx) => `  ${idx + 1}. ${item}`)
        );
      });
      masterLines.push(
        ``,
        `========================================================================`,
        `DELIVERY INSTRUCTIONS:`,
        `• Band and weather-wrap each lift separately by drop and floor/zone.`,
        `• Call Site Superintendent Wayne Stevenson 24 hours prior to Moffett / Hiab crane boom delivery.`
      );
      openCustomVaultPdfOnScreen(
        `Master 5-Drop Material Takeoff (Drops #1–#5 • Dick's Lumber #52603-KEYSTONE)`,
        `${job.jobId}_ALL_5_DROPS_Dicks_Lumber_Master_Order_List.pdf`,
        `All 13 IFC Sheets (A-101..E-101) • 5 Staged Delivery Drops`,
        masterLines.join("\n"),
        ""
      );
      return;
    }

    const d = allDrops.find(x => Number(x.dropNum) === Number(dropNum));
    if (!d) return;
    const lines = [
      `KEYSTONE POSSIBILITIES LTD. (BC HOUSING LICENSED BUILDER #52603)`,
      `DICK'S LUMBER COMMERCIAL DESK — PRINTABLE MATERIAL TAKEOFF ORDER LIST`,
      `========================================================================`,
      `SUPPLIER ACCOUNT : Dick's Lumber & Building Supplies — Account #52603-KEYSTONE`,
      `DELIVERY SITE    : ${job.address} (${job.jobId}) | Permit #${job.permitNum || "BP2026-0419"}`,
      `SUPERINTENDENT   : Wayne Stevenson — (604) 848-9688`,
      `PACKAGE / DROP   : ${d.title}`,
      `BLUEPRINT SHEETS : ${d.sheets}`,
      `DELIVERY WINDOW  : ${d.deliveryStage}`,
      `========================================================================`,
      ``,
      `ITEMIZED LUMBER, ENGINEERED WOOD & HARDWARE ORDER LIST (ZERO PRICING ON FIELD TICKET):`,
      ...d.items.map((item, idx) => `  ${idx + 1}. ${item}`),
      ``,
      `========================================================================`,
      `DELIVERY INSTRUCTIONS:`,
      `• Band and weather-wrap each lift separately by floor/zone.`,
      `• Call Site Superintendent Wayne Stevenson 24 hours prior to Moffett / Hiab crane boom delivery.`
    ];
    openCustomVaultPdfOnScreen(
      `${d.title} (Dick's Lumber #52603-KEYSTONE)`,
      `${job.jobId}_${d.id}_Dicks_Lumber_Order_List.pdf`,
      `${d.sheets} • ${d.deliveryStage}`,
      lines.join("\n"),
      ""
    );
  };

  const _v13RenderMaterialsList = renderMaterialsList;
  renderMaterialsList = function() {
    _v13RenderMaterialsList();
    const pane = document.getElementById("kp-page-5");
    const acc = document.getElementById("kp-material-accordions");
    if (!pane || !acc) return;

    let dropsBox = document.getElementById("kp-v15-dicks-lumber-5drops-box");
    if (!dropsBox) {
      dropsBox = document.createElement("div");
      dropsBox.id = "kp-v15-dicks-lumber-5drops-box";
      dropsBox.style.cssText = "background:#080c14; border:1.5px solid rgba(212,175,55,0.58); border-radius:14px; padding:15px 18px; margin-bottom:14px;";
      acc.parentNode.insertBefore(dropsBox, acc);
    }

    const all13Sheets = [
      ...(blueprintSheets.arch || []),
      ...(blueprintSheets.eng || [])
    ];

    dropsBox.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px; padding-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.12);">
        <div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
            <span class="kp-badge-pill kp-badge-gold">BLUEPRINT-TO-LUMBER ENGINE &bull; 13 IFC SHEETS (A-101..E-101)</span>
            <span class="kp-badge-pill kp-badge-white">DICK'S LUMBER ACCOUNT #52603-KEYSTONE</span>
          </div>
          <h2 class="kp-section-h2" style="font-size:1.05rem; margin:0;">
            5-Drop Printable Dick's Lumber Material Takeoff Lists Extracted Off Approved Plans
          </h2>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" onclick="openDicksLumberDropPdf('ALL')" class="kp-gold-btn kp-pill-sm">
            📄 Open Master Drop #1–#5 Takeoff PDF
          </button>
          <button type="button" onclick="shipMaterialTakeoffToSupplier('All 5 Drops — Master Framing & Envelope Takeoff')" class="kp-secondary-btn kp-pill-sm">
            🚚 Dispatch All 5 Drops to Dick's Lumber (#52603)
          </button>
        </div>
      </div>

      <!-- 13 Blueprint Sheets Quick Pill Bar -->
      <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:12px; background:#05070b; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:8px 12px;">
        <span style="font-size:0.72rem; font-weight:800; color:#d4af37; text-transform:uppercase; margin-right:4px;">13 IFC Blueprint Sheets:</span>
        ${all13Sheets.map(s => `
          <span style="font-size:0.72rem; font-weight:800; color:#ffffff; background:#0b0f17; border:1px solid rgba(212,175,55,0.38); border-radius:9999px; padding:3px 9px;" title="${escapeHtml(s.title)}">
            ${escapeHtml(s.id)}
          </span>
        `).join("")}
      </div>

      <!-- 5 Printable Dick's Lumber Delivery Drops -->
      <div style="display:flex; flex-direction:column; gap:8px;">
        ${(window.KP_DICKS_LUMBER_5_DROPS || []).map(d => `
          <div style="background:#05070b; border:1px solid rgba(212,175,55,0.42); border-radius:10px; padding:10px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <div style="min-width:0; flex:1;">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="kp-badge-pill kp-badge-gold">${escapeHtml(d.id)}</span>
                <span style="font-size:0.88rem; font-weight:800; color:#ffffff;">${escapeHtml(d.title)}</span>
              </div>
              <div style="font-size:0.74rem; color:#cbd5e1; margin-top:3px;">
                📐 <strong style="color:#ffffff;">${escapeHtml(d.sheets)}</strong> &bull; 🗓️ ${escapeHtml(d.deliveryStage)} &bull; 📦 ${d.items.length} Line Items Ready for Order
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-shrink:0;">
              <button type="button" onclick="openDicksLumberDropPdf(${d.dropNum})" class="kp-gold-btn kp-pill-sm">
                📄 Open / Print PDF List
              </button>
              <button type="button" onclick="shipMaterialTakeoffToSupplier('${escapeHtml(d.title)}')" class="kp-secondary-btn kp-pill-sm">
                🚚 Send to Dick's Lumber
              </button>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  };

  try {
    injectPortalV15CanonicalStyles();
    injectTopHeroBannerIntoPortal();
    purgeDefaultSampleRevisionsEverywhere();
    saveState(true);
    renderAllPortalComponents();
  } catch (e) {
    console.warn("v15 init warning:", e);
  }
})();
