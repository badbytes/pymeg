'''db format'''
##
##
##    
##
##def patient():
##    dir = {}
##    dir['id']=11
##    dir['last_name']=16
##    dir['first_name']=16
##    dir['middle_name']=16
##    dir['birth_date']=16
##    dir['last_name']=16
##    dir['last_name']=16
##    dir['last_name']=16
##    dir['last_name']=16
##    dir['last_name']=16
##    dir['last_name']=16
##
##    
##    
##
##record patient {
##		/* personal info */
##		unique  key char id[11];
##		char 	last_name[16];
##		char 	first_name[16];
##		char 	middle_name[16];
##		long 	birth_date;	/*stored in yyyymmdd format */
##		char 	ethnic[13];
##		char 	home_phone[16];
##		char 	work_phone[16];
##		char 	address[41];
##		char	apartment_number[5];
##		char 	city[26];
##		char 	state[21];
##		char 	country[16];
##		char 	zip_code[11];
##		char	nationality[16];
##		int	handedness;
##		int 	gender;
##
##		/* other info */
##		char 	empl_name[36];
##		char 	institution_id[26];
##		char	height[6];
##		char	weight[6];
##
##		/* undefined additional information */
##		/* labels has extra ":" character */
##		char	added_label[8][16];
##		char	added_data[8][46];
##
##		/* use count for record locking */
##		int	patient_used_cnt;
##	}
##
##	record scan {
##		key char scan_name[26];
##		/* use count for record locking */
##		int	scan_used_cnt;
##		int     scan_data_type;   /* MEG or MRI */
##		char	acq_param[8192][1];
##	}
##
##	record scan_param {
##		key char	scan_param_name[11];	/* change 10 to 11 */ 
##		char	scan_acq_param[8192][1];
##	}
##
##	record image_scan {
##                key char mri_name[42];
##                int     image_type;     /* MR or CT or dipole*/
##                int     mri_scan_type;  /* coronal, axial, sagittal */
##                char    scan_date[17];  /* mm/dd/yyyy hh:mm */
##                char    trans_date[17]; /* mm/dd/yyyy hh:mm */
##                int     mri_transform;  /* 1: transform file exist */
##                int     num_slices;	/* number of slices or dipoles */
##                int     mri_archived;
##                int     mri_used_cnt;
##                long    mri_hd_size;
##                long    mri_od_size;
##                char    mri_media_name[256];
##                char    mri_host_name[16];
##                char    mri_file_system[16];
##		int     mri_creator;
##                long    mri_creation_time;
##                long    mri_archive_time;
##                long    mri_hd_modify_time;
##                long    mri_od_modify_time;
##                char    mri_reserve[16];
##        }
##
##	record session {
##		key char session_name[42];
##		long 	session_date;	/*stored in yyyymmdd format */
##		char 	operator_name[9];
##
##		/* use count for record locking */
##		int	session_used_cnt;
##	}
##
##	record session_run {
##		key char run_name[55];
##		/* use count for record locking */
##		int	run_used_cnt;
##		char	run_media_name[256];
##
##		char	run_host_name[16];
##		char	run_file_system[16];
##
##		long 	config_archive_time;
##		long 	config_hd_modify_time;
##		long 	config_od_modify_time;
##		long	config_hd_file_size;
##		long	config_od_file_size;
##
##		long 	hs_archive_time;
##		long 	hs_hd_modify_time;
##		long 	hs_od_modify_time;
##		long	hs_hd_file_size;
##		long	hs_od_file_size;
##
##		int	run_hs_exists;     /* head shape exist in run dir */
##		int	run_archived;      /* run already archived? */
##	}
##
##	record data_info {
##		key char data_name[129];
##		int	pdf_creator;
##		long	pdf_creation_time;
##		int 	pdf_archived;
##		int	pdf_arch_media_num;
##		int	pdf_locked;
##		long	pdf_archive_time;
##		long	pdf_hd_modify_time;
##		long	pdf_od_modify_time;
##		long	pdf_hd_file_size;
##		long	pdf_od_file_size;
##
##		/* use count for record locking */
##		int	pdf_used_cnt;
##		char	pdf_param[100][1];
##	}
##
##	record text80 {
##		int  text_order;
##		char text[80];
##	}
##
##	record user {
##		char user_id[16];
##	}
##
##	/* record stores selection info */
##	record sel_rec {
##		char sel_data[129]; 
##	}
##
##	/* record saves user's defined labels */
##	record labels {
##		char label_set_name[16];
##		char label[8][16];
##	}
##	
##	/* record stores data filter information */
##        record iir_filter {
##                char filter_name[16];
##                int filter_used_cnt;    /* control record deletion */
##                int total_filters;
##                struct  {
##                        int     ftype;  /* filter type */
##                        int     enable; /* 1=enable filter, 0=disable filter */
##                        float  fh;     /* high edge filter frequency (Hz) */
##                        float  fl;     /* low edge filter frequency (Hz) */
##                        float  rate;   /* sample rate (Hz or points/second) */
##                        float  bwn;    /* noise bandwidth (Hz) */
##                        int     iir_order;     /* number of coefficient pairs */                        float  num[20]; /* numerator iir coefficients */
##                        float  den[20]; /* denominator iir coefficients*/
##                } iir_param[8];
##        }
##
##	set label_of_user {
##		order ascending;
##		owner user;
##		member labels by label_set_name;
##	} 
##
##	set user_of_root {
##		order last;
##		owner system;
##		member user;
##	} 
##
##	set primary_sel_of_user {
##		order last;
##		owner user;
##		member sel_rec;
##	} 
##
##	set patient_of_root {
##		order ascending;
##		owner system;
##		member patient by id;
##	} 
##
##	set scan_of_patient {
##		order ascending;
##		owner patient;
##		member scan by scan_name;
##	} 
##
##	set session_of_scan {
##		order ascending;
##		owner scan;
##		member session by session_name;
##	} 
##
##	set image_of_scan {
##		order ascending;
##		owner scan;
##		member image_scan by mri_name;
##	} 
##
##	set comment_of_session {
##		order ascending;
##		owner session;
##		member text80 by text_order;
##	}
##
##	set comment_of_mriscan {
##		order ascending;
##		owner image_scan;
##		member text80 by text_order;
##	}
##
##	set run_of_session {
##		order ascending;
##		owner session;
##		member session_run by run_name;
##	} 
##
##	set comment_of_run {
##		order ascending;
##		owner session_run;
##		member text80 by text_order;
##	}
##
##	set data_of_run {
##		order ascending;
##		owner session_run;
##		member data_info by data_name;
##	} 
##
##	/* patient's history text */
##	set history_notes {
##		order ascending;
##		owner patient;
##		member text80 by text_order;
##	}
##
##	/* filter path */
##        set filter_of_root {
##                order ascending;
##                owner system;
##                member iir_filter by filter_name;
##        }
##}